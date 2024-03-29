"""
Project     :   Linkscribe
Package     :   webScrap
Description :   This package sets the router to get the Title, webpage screenshot, 
                and private method for webScraping  
Modification History: 
*********************************************************
Date            Author          Modification
27-03-2024      jdmunoz         Creation
*********************************************************
"""
# Libraries 
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import imgkit
import os


# Web Scraping libraries 
from bs4 import BeautifulSoup
import requests
# -----


# Package constants
output_file = "page_preview.jpg"
# -----


# model entry schema 
class URLEntry(BaseModel):
    inURL: str
    def url_var(self):
        return self.inURL      


# Private methods
"""
Project     :   Linkscribe
Package     :   webScrap 
Method      :   webScraping   
Description :   This method gets the pure text from webpages
Inputs      :   url --> URL for web-scraping
Modification History: 
*********************************************************
Date            Author          Modification
27-03-2024      jdmunoz         Creation
*********************************************************
"""
def webScraping(inUrl):
    # Send a GET request to the URL
    print(inUrl)
    response = requests.get(inUrl)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')        
        # Extract text from the parsed HTML
        text = soup.get_text(separator='\n', strip=True)        
        return text
    else:
        # If the request was not successful, print an error message
        RuntimeError(f"Error: Unable to retrieve content from {inUrl}. Status code: {response.status_code}")
        return None
    

"""
Project     :   Linkscribe
Package     :   webScrap 
Method      :   delpreview   
Description :   This method deletes the output_file 
Modification History: 
*********************************************************
Date            Author          Modification
27-03-2024      jdmunoz         Creation
*********************************************************
"""
def delpreview(inuFile):
    if os.path.exists(output_file):
        os.remove(inuFile)


"""
Project     :   Linkscribe
Package     :   webScrap 
Method      :   getTitle   
Description :   This method deletes the output_file 
Modification History: 
*********************************************************
Date            Author          Modification
27-03-2024      jdmunoz         Creation
*********************************************************
"""
def getTitle(url):

    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    }
    # send the get request to url 
    response = requests.get(url,headers=headers)

 # Check if the request was successful
    if response.status_code == 200:       

        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the title 
        title_tag = soup.find('title')

        # Extract and return title if found 
        if title_tag:
            return  title_tag.text.strip()
        else:
            return "Title not found"
    else:
        return f"Error fetching the URL status {response.status_code}"   

# ------    


"""
Project     :   Linkscribe
Package     :   webScrap 
Method      :   generate_url_to_image   
Description :   This method takes a screenshot from webpages
Inputs      :   url --> URL for web preview screenshot
Modification History: 
*********************************************************
Date            Author          Modification
27-03-2024      jdmunoz         Creation
*********************************************************
"""
def generate_url_to_image(url, output_file=output_file):
    try:
        #print(html_content)
        imgkit.from_url(url, output_file)

        print(f"Image saved as '{output_file}'")
    except Exception as e:
        print(f"Error: {e}")     

# creating the router for the API 
router = APIRouter()

"""
Project     :   Linkscribe
Package     :   LScribe_model_api 
Method      :   get_image 
Description :   this method is called by /image in the forwarded port as post, 
                so it gets preview screenshot from url by calling a private 
                method URL_preview  
Modification History: 
*********************************************************
Date            Author          Modification
26-03-2024      jdmunoz         Creation
*********************************************************
"""
@router.post("/image")
async def get_image(data: URLEntry):
    # Deleting the file from previous execution
    delpreview(output_file)

    # getting the url and preview image 
    url_input = data.url_var()

    generate_url_to_image(url_input)

    # validation of the preview existence   
    if not os.path.exists(output_file):
        raise HTTPException(status_code=404, detail="Image not found")
    
    return FileResponse(output_file)


"""
Project     :   Linkscribe
Package     :   LScribe_model_api 
Method      :   get_title 
Description :   this method is called by /title in the forwarded port as post, 
                so it gets Title from url by calling a private 
                method getTitle  
Modification History: 
*********************************************************
Date            Author          Modification
26-03-2024      jdmunoz         Creation
*********************************************************
"""
@router.post("/title")
async def get_title(data: URLEntry):

    inUrl = data.url_var()
    title = getTitle(inUrl)

    return JSONResponse(content={"Title": title })

    

