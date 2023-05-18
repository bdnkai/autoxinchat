from fastapi import FastAPI
from pydantic import BaseModel
from process_users import process_image, process_debug
import difflib



app = FastAPI()

class Player(BaseModel):
    names: list = ['ALCONTECE', 'AlieenMax', 'AlphaGo1 ', 'aMirM', 'AnneAnnePro', 'Bagorlz', 'BDN', 'Bigbah', 'BruceLee', 'Cah', 'Carly', 'Catdog', 'CaydeA', 'ChiPowDew', 'CrazyPixelsz', 'DaytonaTwin', 'Demencial', 'Demente', 'DemonBlast', 'Domino', 'Dro', 'EdMachinax', 'Eros', 'Escobart', 'EssMDee', 'EVAxNERVx', 'EvilLynn', 'Febreza', 'G0nee', 'Gabranx', 'GoSup3rbPvP', 'GuiZambrana', 'Gwapoy', 'ICHAM', 'JackBui', 'JudgeGilman', 'Kaminari', 'KanG', 'KneeHowMang肏你媽', 'Lighty02', 'Liyue', 'Loptous', 'Luxo', 'MaouSama', 'McCornChad', 'MelSouL', 'MOWZ', 'MRasec', 'MuDDAFuQA', 'Netoroots', 'oblik', 'OokamiHoro', 'Oppaii', 'PhoenixH', 'Psychez', 'Ricest', 'Rovi', 'RoyalG', 'S0JU', 'sexypants', 'Shinokgod', 'Shunli', 'SKR7', 'SpringRain', 'ssdcarl', 'TayTawan', 'Tragzy', 'Vizualz', 'Voodood', 'Witcha90', 'Xasley', 'Yofella', 'Yonzilla', 'Zcalius', '你爸爸', '你野', '叫我', '破天命', '聪明绝顶的pp', '贪生恶杀', 'ME请你妈ME傅你妈', 'ninefingers', 'yingying']


class Threshold(BaseModel):
    rate: float = 0.54


current_threshold = Threshold()
current_player = Player()
players = []

@app.get("/")
def index():
    return {"title": "Welcome to AutoXinChat"}


@app.get("/process")
async def get_autoxinchat(url : str):
    results = process_image(url, thresh_rate=current_threshold.rate, player_names=current_player.names)
    return {"names": results}


@app.get("/debug")
async def get_autoxindebug(url : str):
    results = process_debug(url, thresh_rate=current_threshold.rate, player_names=current_player.names)
    return {"message": results}


@app.get("/get_list")
async def get_autoxinplayer():
    results = current_player.names
    return {"names": current_player.names}


@app.post("/add_player")
async def add_player(player: Player):
    current_player.names.extend(player.names)
    return {"message": "Player(s) have been added", "new_players": player.names}



@app.delete("/remove_player/{player_name}")
async def remove_player(player_name: str):
    global current_player

    # Use difflib to find close matches
    close_matches = difflib.get_close_matches(player_name, current_player.names)

    if close_matches:
        current_player.names = [name for name in current_player.names if name not in close_matches]
        return {"message": "Players have been removed", "removed_players": close_matches}
    else:
        return {"message": "No close matches found for player", "player_name": player_name}


@app.patch("/update_threshold")
async def update_threshold(threshold: Threshold):
    global current_threshold
    current_threshold = threshold
    return {"message": "Threshold updated", "new_threshold": threshold}

