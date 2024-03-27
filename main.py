"""
Project     :   Linkscribe
Package     :   main 
Description :   This Package has the objective to start the web server using uvicorn using the  
Modification History: 
*********************************************************
Date            Author          Modification
25-03-2024      jdmunoz         Creation
*********************************************************
"""

# Libraries 
import uvicorn # web server
import os
# ----

# Running uvicorn server with the api app
if __name__ == "__main__":
    # run the method to star the API
    uvicorn.run(
        "api:app", 
        host="0.0.0.0",
        reload=True, 
        port=int(os.environ.get("PORT",8080))
    )
