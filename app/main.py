from fastapi import FastAPI, Request
import time
import concurrent.futures
from process_users import process_image
import requests

app = FastAPI()

@app.get("/")
def index():
    return {"title": "welcome to AutoXinChat"}

@app.get("/process")
async def get_autoxinchat(url : str):
    results = process_image(url)
    return {"names": results}
    