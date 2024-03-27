"""
Project     :   Linkscribe
Package     :   LScribe_model_api 
Description :   This package sets the model router to call the model and make the prediction
Modification History: 
*********************************************************
Date            Author          Modification
25-03-2024      jdmunoz         Creation
*********************************************************
"""

# Libraries 
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel 
from webScrap import webScraping
# -----

# model entry schema 
class LScribeModel(BaseModel):
    inURL: str
    def url_var(self):
        return self.inURL    

# creating the router for the API 
router = APIRouter()

@router.get("/hi")
async def hi_model():
    return {"message": "Hello from the LinkScribe model router "}

"""
Project     :   Linkscribe
Package     :   LScribe_model_api 
Method      :   Predict 
Description :   this method is called by /predict in the forwarded port as post, 
                so it gets the text from the url by calling a private method webScraping  
Modification History: 
*********************************************************
Date            Author          Modification
26-03-2024      jdmunoz         Creation
*********************************************************
"""
@router.post("/predict")
async def predict(request: Request, data: LScribeModel):
    url_input = data.url_var()
    model_input = webScraping(url_input)
    model_LS = request.app.state.model
    model = model_LS["LScribe-Model"]
    predictions = model.predict([model_input])
    return  JSONResponse(content={"prediction": predictions,
                                  "webText": model_input})


