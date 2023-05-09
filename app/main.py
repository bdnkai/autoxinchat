from fastapi import FastAPI
from app.process_users import process_image
import os

os.environ['LD_LIBRARY_PATH'] = '/app/.apt/usr/lib/'


app = FastAPI()

@app.get("/")
def index():
    return {"title": "welcome to AutoXinChat"}

@app.get("/process")
async def get_autoxinchat(url : str):
    results = process_image(url)
    return {"names": results}
    
    