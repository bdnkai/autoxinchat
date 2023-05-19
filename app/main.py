from fastapi import FastAPI
from pydantic import BaseModel
from process_users import process_image, process_debug
import difflib



app = FastAPI()

class Player(BaseModel):
    names: list = ['AlieenMax', 'AlphaGo1 ', 'aMirM', 'AnneAnnePro', 'Bagorlz', 'BDN', 'Bigbah', 'BruceLee', 'Cah', 'Carly', 'Catdog', 'CaydeA', 'ChiPowDew', 'CrazyPixelsz', 'DaytonaTwin', 'Demencial', 'Demente', 'DemonBlast', 'Domino', 'Dro', 'EdMachinax', 'Eros', 'Escobart', 'EVAxNERVx', 'EvilLynn', 'Febreza', 'G0nee', 'Gabranx', 'GoSup3rbPvP', 'GuiZambrana', 'Gwapoy', 'ICHAM', 'JackBui', 'JudgeGilman', 'Kaminari', 'KanG', 'KneeHowMang肏你媽', 'Lighty02', 'Liyue', 'Loptous', 'Luxo', 'MaouSama', 'McCornChad', 'MelSouL', 'MOWZ', 'MRasec', 'MuDDAFuQA', 'Netoroots', 'oblik', 'OokamiHoro', 'Oppaii', 'PhoenixH', 'Psychez', 'Ricest', 'Rovi', 'RoyalG', 'S0JU', 'sexypants', 'Shinokgod', 'Shunli', 'SKR7', 'SpringRain', 'ssdcarl', 'TayTawan', 'Tragzy', 'Vizualz', 'Voodood', 'Witcha90', 'Xasley', 'Yofella', 'Yonzilla', 'Zcalius', '你爸爸', '你野', '叫我', '破天命', '聪明绝顶的pp', '贪生恶杀', 'ME请你妈ME傅你妈']


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


@app.post("/add_player/{player_name}")
async def add_player(player_name: str):

    current_player.names.extend([player_name])
    return {"message": "Player(s) have been added", "new_players": [player_name]}


@app.delete("/remove_player/{player_name}")
async def remove_player(player_name: str):
    global current_player
    case_name = current_player.names

    # Convert names to lowercase for case-insensitive comparison
    case_name_lower = [name.lower() for name in case_name]
    player_name_lower = player_name.lower()

    # Use difflib to find close matches
    close_matches = difflib.get_close_matches(player_name_lower, case_name_lower, n=1, cutoff=0.85)

    if close_matches:
        # Find the original name from the case-insensitive match
        removed_player = [name for name in case_name if name.lower() == close_matches[0]][0]

        # Remove the player from the list
        current_player.names.remove(removed_player)

        return {"message": "Player has been removed", "removed_player": removed_player}
    else:
        return {"message": "No close match found for player", "player_name": player_name}


@app.patch("/update_threshold")
async def update_threshold(threshold: Threshold):
    global current_threshold
    current_threshold = threshold
    return {"message": "Threshold updated", "new_threshold": threshold}

# if __name__ == '__main__':
#     test = process_debug('https://cdn.discordapp.com/attachments/1106293089552846898/1106474403681808414/image.png',thresh_rate=current_threshold.rate, player_names=current_player.names)
#     print(test)


