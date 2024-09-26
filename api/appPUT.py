from fastapi import FastAPI
from pydantic import BaseModel

class Inuput(BaseModel):
    age : int
    sex : str

app = FastAPI()
@app.put("/predict")
def predict_model(d:Inuput):
    if age<10 or sex=='F':
        return {'survived':1}
    else:
        return {'survived':0}