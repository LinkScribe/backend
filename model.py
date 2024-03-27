"""
Project     :   Linkscribe
Package     :   model 
Description :   This package loads and executes the model to be used in api.py
Modification History: 
*********************************************************
Date            Author          Modification
25-03-2024      jdmunoz         Creation
*********************************************************
"""

# Libraries 
import numpy as np
import typing 

from enum import Enum, auto
from pathlib import Path
from abc import ABC
# ----

# Defining the framework 
class Framework(Enum):
    sklearn = auto()
# ----
    

"""
Project     :   Linkscribe
Package     :   model 
Class       :   Model 
Description :   This class defines the methods to register the model information and execute 
                the predict. 
                This class is out to be used by LinkScribeModel (subclass) as parent class 
Modification History: 
*********************************************************
Date            Author          Modification
25-03-2024      jdmunoz         Creation
*********************************************************
"""
class Model(ABC):

    """
    Method      :   __init__
    Description :   Initial method to set the model information and calls the method load() 
    """
    def __init__(self,
                 model_name: str,
                 model_path: typing.Union[str, Path],
                 framework: Framework,
                 version: int,
                 classes: typing.List[str]
                 ):
        self.model_name = model_name
        self.model_path = model_path
        self.framework  = framework
        self.version    = version
        self.classes    = classes
        self.model      = None

        self.load()
    
    """
    Method      :   load
    Description :   Load the model from the path by calling __load_sklearn_model
    """
    def load(self):
        # Framework validation 
        if self.framework == Framework.sklearn:
            self.__load_sklearn_model()
        else:
            raise ValueError(f"Framework {self.framework} not supported")
    
    """
    Method      :   __load_sklearn_model
    Description :   Load a sklearn model from the path 
    """
    def __load_sklearn_model(self):

        from joblib import load
        self.model = load(self.model_path)

    """
    Method      :   __call__
    Description :   method allows instances of the Model class to be called as if they were functions. 
                    When an instance is called, it internally calls the predict method, 
                    effectively forwarding the call to the predict method
    """
    def __call__(self, X: typing.Any) -> typing.Any:
        return self.predict(X)
    
    """
    Method      :   predict
    Description :   Abstract method, the subclasses of Model must provide a concrete implementation of 
                    the predict method
    """
    def predict(self, X: typing.Any) -> typing.Any:
        raise NotImplementedError(" Subclasses must implement this method")


"""
Project     :   Linkscribe
Package     :   model 
Class       :   LinkScribeModel 
Description :   This class is a subclass of Model class that fills up the model information  
                and set the the predict method for the ML model
Modification History: 
*********************************************************
Date            Author          Modification
26-03-2024      jdmunoz         Creation
*********************************************************
"""
class LinkScribeModel(Model):
    """
    Method      :   __init__
    Description :   Initial method as a subclass of model to register model data, 
                    this method has the model-path 
    """
    def __init__(self, framework: Framework = Framework.sklearn):
        # validate de model framework (by default sklearn)
        if framework == Framework.sklearn:
            model_path = "models/sklearn/Linkscribe.pk"
            version = 1
        else:
            raise ValueError(f"Framework {framework} not supported")
        
        # Defining the output classes 
        classes = ["Adult", "Business/Corporate", "Computers and Technology",
       "E-Commerce", "Education", "Food", "Forums", "Games",
       "Health and Fitness", "Law and Government", "News", "Photography",
       "Social Networking and Messaging", "Sports", "Streaming Services",
       "Travel"]
        
        # Model name
        name = "LScribe-Model"
        
        # calling the father class
        super().__init__(name,model_path,framework,version, classes)

    """
    Method      :   predict
    Description :   makes the prediction when called
    """
    def predict(self, X):
        # output variable
        outputs = []

        # validates the framework
        if self.framework == Framework.sklearn: 
            # makes the prediction
            prediction = int(self.model.predict(X))
            outputs.append(self.classes[prediction])
            
        # return results
        return outputs



    

        


         
