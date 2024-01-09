from fastapi import FastAPI
from enum import Enum


# TO reload this app use - uvicorn main:app --reload   --main - name of the file, app - name of this app
appName = FastAPI()

@appName.get("/")
@appName.get("/home")
async def root():
    return {"message": "Hello, the API is made to expose game related information as per genre"}

'''path parameters, query parameters, request body, using validations in these parameters'''




class ModelName(str, Enum):
    alexnet = "alexnet1"
    resnet = "resnet2"
    lenet = "lenet3"


app = FastAPI()


@appName.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    print(model_name.value)
    print(model_name)
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": model_name.value}

    if model_name == ModelName.lenet:
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}
