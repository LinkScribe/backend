"""
Project     :   Linkscribe
Package     :   api  
Description :   Principal package of the Linkscribe backend algorithm. 
                Here the ML model is loaded, the web-scraping and prediction is called
Modification History: 
*********************************************************
Date            Author          Modification
25-03-2024      jdmunoz         Creation
*********************************************************
"""

# libraries 
from fastapi import FastAPI
from contextlib import asynccontextmanager
from model import LinkScribeModel, Framework

# Backend routers 
from LScribe_model_api import router as LScribe_model_router
from webScrap import router as webInfo
from fastapi.middleware.cors import CORSMiddleware
# ------------------------

"""
Project     :   Linkscribe
Package     :   api 
Method      :   lifespan 
Description :   This method load the model to be used by the app set by FastAPI library.
                The model is register in a dict() as "LScribe-Model"
Modification History: 
*********************************************************
Date            Author          Modification
25-03-2024      jdmunoz         Creation
*********************************************************
"""
@asynccontextmanager
async def lifespan(app: FastAPI):

    # Loading the ML model 
    # Create a dictionary to save a ref to the registered model
    app.state.model = dict()

    # Register the model in the model dictionary 
    linkS_model = LinkScribeModel(framework=Framework.sklearn)

    app.state.model["LScribe-Model"] = linkS_model

    yield
    # Clean up the ML models and release the resources

# creating the API
app = FastAPI(lifespan=lifespan)

app.include_router(LScribe_model_router, prefix="/LScribe-Model")
app.include_router(webInfo, prefix="/webInfo")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://34.16.170.210","http://localhost:4200"],  # Reemplaza con la URL de tu aplicación Angular
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome LinkScribe"}
