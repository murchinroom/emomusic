from fastapi import FastAPI, UploadFile
from pydantic import BaseModel
from music_predict import MusicEmotionRecognition
import tempfile

app = FastAPI()
predictor = MusicEmotionRecognition()

@app.get("/")
async def root():
    return {"hello": "MusicEmotionRecognition"}

# @app.get("/predictpath")
# async def predict(data_path: str):
#     pipeline = MusicEmotionRecognition()
#     a, v = pipeline.predict_data([data_path])
#     return {"arouse": a[0], "valence": v[0]}

class MusicEmotion(BaseModel):
    arouse: float
    valence: float

# upload file -> predict
@app.post("/predictmp3")
async def predictfile(file: UploadFile) -> MusicEmotion:
    # save tmp file
    with tempfile.NamedTemporaryFile() as tmp:
        tmp.write(file.file.read())

        a, v = predictor.predict_data([tmp.name])
        return MusicEmotion(arouse=a[0], valence=v[0])
