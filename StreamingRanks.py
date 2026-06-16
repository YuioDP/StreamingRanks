from flask import Flask, jsonify
import requests
import os
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)


API_KEY = os.getenv("RIOT_API_KEY")


# Página de prueba
@app.route("/")
def home():
    return "Servidor Riot funcionando"


# Ejemplo:
# /player/Yuio/LAN/la1

@app.route("/player/<name>/<tag>/<platform>")
def player(name, tag, platform):

    headers = {
        "X-Riot-Token": API_KEY
    }


    # ==========================
    # 1. Obtener cuenta Riot
    # ==========================

    account = requests.get(
        f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{name}/{tag}",
        headers=headers,
        timeout=20
    )


    if account.status_code != 200:
        return jsonify({
            "error": "No se encontró la cuenta Riot",
            "response": account.json()
        }), account.status_code


    account_data = account.json()

    puuid = account_data["puuid"]



    # ==========================
    # 2. Obtener ranked
    # ==========================

    ranked = requests.get(
        f"https://{platform}.api.riotgames.com/lol/league/v4/entries/by-puuid/{puuid}",
        headers=headers,
        timeout=20
    )


    if ranked.status_code != 200:
        return jsonify({
            "error": "No se pudo obtener ranked",
            "response": ranked.json()
        }), ranked.status_code



    ranked_data = ranked.json()



    # ==========================
    # 3. Buscar Solo/Duo
    # ==========================

    solo_ranked = None


    for queue in ranked_data:

        if queue["queueType"] == "RANKED_SOLO_5x5":
            solo_ranked = queue
            break



    if solo_ranked is None:

        return jsonify({
            "error": "La cuenta no tiene ranked Solo/Duo"
        })



    # ==========================
    # 4. Calcular datos
    # ==========================

    wins = solo_ranked["wins"]

    losses = solo_ranked["losses"]

    total_games = wins + losses


    winrate = round(
        (wins / total_games) * 100,
        2
    )



    # ==========================
    # 5. Respuesta final
    # ==========================


    return jsonify({

        "riot_id": f"{name}#{tag}",

        "region": platform,

        "tier": solo_ranked["tier"],

        "rank": solo_ranked["rank"],

        "lp": solo_ranked["leaguePoints"],

        "wins": wins,

        "losses": losses,

        "winrate": winrate

    })



app.run(debug=True)