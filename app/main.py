from fastapi import FastAPI
from process_users import process_image




app = FastAPI()

@app.get("/")
def index():
    return {"title": "welcome to AutoXinChat"}



@app.get("/process")
async def get_autoxinchat(url : str):
    results = process_image(url)
    return {"names": results}


if __name__ == '__main__':
    process_image('https://cdn.discordapp.com/attachments/1106293089552846898/1106474957313155122/image.png')