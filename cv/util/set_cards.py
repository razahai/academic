from pathlib import Path
import requests

SET_URL = "https://www.setgame.com/sites/all/modules/setgame_set/assets/images/new/"

for n in range(1, 82):
    path = Path(f"./in/cards/{n}.png")

    with open(path, "wb") as file:
        res = requests.get(f"{SET_URL}{n}.png", stream=True)

        if not res.ok:
            print(res)

        for block in res.iter_content(1024):
            if not block:
                break

            file.write(block)
        
