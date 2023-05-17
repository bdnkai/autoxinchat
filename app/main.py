from fastapi import FastAPI
from pydantic import BaseModel
from process_users import process_image, process_debug



app = FastAPI()



class Threshold(BaseModel):
    rate: float = 0.54


current_threshold = Threshold()


@app.get("/")
def index():
    return {"title": "Welcome to AutoXinChat"}


@app.get("/process/")
async def get_autoxinchat(url : str):
    results = process_image(url, thresh_rate=current_threshold.rate)
    return {"names": results}

@app.get("/debug")
async def get_autoxinchat(url : str):
    results = process_debug(url, thresh_rate=current_threshold.rate)
    return {"message": results}

# @app.post("/add_player")
# async def update_threshold(threshold: Threshold):
#     global current_threshold
#     current_threshold = threshold
#     return {"message": "Threshold updated", "new_threshold": threshold}


@app.patch("/update_threshold")
async def update_threshold(threshold: Threshold):
    global current_threshold
    current_threshold = threshold
    return {"message": "Threshold updated", "new_threshold": threshold}
