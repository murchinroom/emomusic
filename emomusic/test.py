"""
This module containg all the necessary methods for testing the models trained to predict values
for valence and arousal.
"""
import os
import torch
import numpy as np
from models import AudioNet
from data_loader import normalize_mfccs 


class Tester:
    """
    Methods for testing are defined in this class.

    Attributes:
        dimension (str): specifies the type of output predicted by the model
        test_loader: loading and batching the data in test set
        model: AudioNet model with parameters according to `dimension`
        valence_dict, arousal_dict, quadrants_dict: dictionaries containing data needed for computing
        performance metrics and visualization
    """
    def __init__(self, args):

        self.dimension = args.dimension

        self._data_dir = args.data_dir
        self._models_dir = args.models_dir
        self._plots_dir = args.plots_dir
        self._device = torch.device(args.device if torch.cuda.is_available() else 'cpu')

        #self.test_loader = make_testing_loader(self._data_dir)

        if self.dimension == 'both':
            self._params_dict = args.params_dict
            self.model = AudioNet(self._params_dict).to(self._device)
        else:
            self._valence_params_dict = args.valence_params_dict
            self._arousal_params_dict = args.arousal_params_dict

            self.valence_model = AudioNet(self._valence_params_dict).to(self._device)
            self.arousal_model = AudioNet(self._arousal_params_dict).to(self._device)

        self.valence_dict = dict()
        self.arousal_dict = dict()
        self.quadrants_dict = dict()

    
    def load_model_2d(self):
        """
        Method to load the pretrained model to predict values for both valence and arousal dimensions.
        """
        model_path = os.path.join(self._models_dir, 'model_{:s}.pt'.format(self.dimension))
        self.model.load_state_dict(torch.load(model_path,map_location=torch.device('cpu')))

    
    def my_test(self,tem):    
        test_data = np.array(tem)
        mfcc_mean = torch.tensor(-3.9429)
        mfcc_std = torch.tensor(77.2486)
        test_data = torch.tensor(test_data.astype(np.float32))
        test_data = normalize_mfccs(test_data, mfcc_mean, mfcc_std)
        pred_annotations = []
        self.model.eval()
        data = test_data
        # Freeze gradients
        with torch.no_grad():
            #for batch_idx, (data) in enumerate(test_loader):
                # Move dat
            data = data.to(self._device)
            # Make predictions for valence and arousal
            output = self.model(data)
            pred_annotations.extend(output.cpu().detach().numpy())
        pred_annotations = np.array(pred_annotations)
        pred_valence = np.array([annot[0] for annot in pred_annotations])
        pred_arousal = np.array([annot[1] for annot in pred_annotations])
        #print(pred_arousal)
        #print(pred_valence)
        return pred_arousal,pred_valence

    