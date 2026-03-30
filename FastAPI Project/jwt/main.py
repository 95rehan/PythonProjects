from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from create_jwt import create_access_token
from validate_jwt import validate_token
import requests
import yaml

app = FastAPI()

# -------------------------------
# 🔧 Load config
# -------------------------------
with open("secret.yaml", "r") as f:
    config = yaml.safe_load(f)

WEATHER_API_KEY = config.get("WEATHER_API_KEY")
FOOTBALL_API_KEY = config.get("FOOTBALL_API_KEY")

# -------------------------------
# 🔐 Security setup
# -------------------------------
security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    result = validate_token(token)

    if not result["valid"]:
        raise HTTPException(status_code=401, detail=result["error"])

    return result["data"]


# -------------------------------
# 🔑 LOGIN (creates JWT)
# -------------------------------
@app.post("/login")
def login(user_id: str, name: str, role: str = "user"):
    # In real world → validate from DB
    token = create_access_token(user_id, name, role)

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# -------------------------------
# 🔐 Protected test endpoint
# -------------------------------
@app.get("/me")
def get_me(user=Depends(get_current_user)):
    return {
        "message": "User authenticated",
        "user": user
    }


# -------------------------------
# 🌤 Weather API
# -------------------------------
@app.get("/weather")
def get_weather(city: str, user=Depends(get_current_user)):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"

    response = requests.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="City not found")

    data = response.json()

    return {
        "city": city,
        "temperature": data["main"]["temp"],
        "condition": data["weather"][0]["description"],
        "humidity": data["main"]["humidity"],
        "requested_by": user["name"]
    }


# -------------------------------
# ⚽ EPL Players API
# -------------------------------
@app.get("/epl-players")
def get_players(team: str, user=Depends(get_current_user)):

    team_map = {
        "arsenal": 57,
        "chelsea": 61,
        "manchester city": 65,
        "manchester united": 66,
        "liverpool": 64,
        "tottenham": 73,
    }

    team_id = team_map.get(team.lower())

    if not team_id:
        raise HTTPException(status_code=400, detail="Team not supported")

    url = f"https://api.football-data.org/v4/teams/{team_id}"

    headers = {
        "X-Auth-Token": FOOTBALL_API_KEY
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Error fetching team data")

    data = response.json()

    players = [
        {
            "name": player["name"],
            "position": player.get("position"),
            "nationality": player.get("nationality")
        }
        for player in data.get("squad", [])
    ]

    return {
        "team": team,
        "total_players": len(players),
        "players": players,
        "requested_by": user["name"]
    }