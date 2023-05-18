from typing import Tuple
import os
from numpy import ndarray
from data_preprocessing import DataPreprocessor
from test import Tester
import argparse


class MusicEmotionRecognition:
    def __init__(self):
        self.args_from_json = {'data_dir': 'Data', 'deam_dir': 'Data/DEAM_dataset', 'font_dir': 'Font', 'models_dir': 'Models', 'plots_dir': 'Plots', 'audio_extension': 'mp3', 'sample_rate': 44100, 'device': 'cuda', 'mode': 'preprocess', 'dimension': 'both', 'params_dict': {'in_ch': 20, 'num_filters1': 32, 'num_filters2': 64, 'num_hidden': 256, 'out_size': 2}, 'valence_params_dict': {'in_ch': 20, 'num_filters1': 32, 'num_filters2': 64, 'num_hidden': 64, 'out_size': 1}, 'arousal_params_dict': {'in_ch': 20, 'num_filters1': 32, 'num_filters2': 32, 'num_hidden': 64, 'out_size': 1}, 'lr_init': 0.001, 'lr_decay': 0.1, 'decay_interval': 1000, 'weight_decay': 0.01, 'num_epochs': 2000, 'log_interval': 1}
        self.args = argparse.Namespace(**self.args_from_json)
        self.args.data_pt = ""
        self.args.models_dir = os.path.join(os.path.dirname(__file__), "Models")
        self.tester = Tester(self.args)
        self.tester.load_model_2d()


    def predict_data(self, data_path) -> Tuple[ndarray, ndarray]:
        """music file -> emotion

        args:
            data_path: ["/path/to/music.mp3"]
        return:
            ([arouse], [valence])
        """
        if self.args.mode == 'preprocess':
            self.args.data_pt = data_path
            data_preprocessor = DataPreprocessor(self.args)
            data_preprocessor.get_test_data_info()
            tem = data_preprocessor.get_waveforms()
            a,v = self.tester.my_test(tem)
            return a,v


if __name__ == '__main__':
    
    data_path = [
            "./songs/十局上半.mp3", 
            "./songs/庐州月.mp3", 
            "./songs/唯一-告五人.mp3", 
            "./songs/你要跳舞吗.mp3",
            "./songs/义勇军.mp3",
            "./songs/好运来.mp3",
            "./songs/猪猪侠.mp3",
            "./songs/恭喜发财.mp3"]

    pipeline = MusicEmotionRecognition()
    
    for d in data_path:
        print(d, end="\t")
        a, v = pipeline.predict_data([d])
        # print(a, v)
        print("arouse: {}\tvalence: {}".format(a, v))



