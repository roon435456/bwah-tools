from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class NameChangeRequest(BaseModel):
    token: str
    username: str

@app.post("/api/change-name")
async def change_name(payload: NameChangeRequest):
    title_id = "11dd05"
    url = f"https://{title_id}.playfabapi.com/Client/UpdateUserData"
    
    headers = {
        "Host": f"{title_id}.playfabapi.com",
        "User-Agent": "UnityPlayer/2022.3.55f1 (UnityWebRequest/1.0, libcurl/8.10.1-DEV)",
        "X-ReportErrorAsSuccess": "true",
        "X-PlayFabSDK": "UnitySDK-2.206.241122",
        "X-Authorization": payload.token,
        "Content-Type": "application/json",
        "X-Unity-Version": "2022.3.55f1"
    }
    
    playfab_payload = {
        "CustomTags": None,
        "Data": {
            "GameUsername": payload.username
        },
        "KeysToRemove": None,
        "Permission": None,
        "AuthenticationContext": None
    }
    
    try:
        response = requests.post(url, json=playfab_payload, headers=headers)
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
