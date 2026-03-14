import os
import json
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from pydantic import BaseModel
from mistralai.client import Mistral
from dotenv import load_dotenv

# ---
# Initial setup

back_dir = Path(__file__).parent
front_dir = back_dir / ".." / "frontend"
load_dotenv()
client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))
app = FastAPI()

# ---
# GET requests

@app.get("/")
async def serve_index():
    return FileResponse(front_dir / "index.html")
@app.get("/typo-checker")
async def serve_index():
    return FileResponse(front_dir / "typo-checker.html")

# ---
# Client request schema
class AnalysisRequest(BaseModel):
    sentence: str
    # intended_meaning: str
    # tone: str
    # context: str

# ---
# AI response schema
# class TypoCheckerResponse(BaseModel):



@app.post("/api/typo-checker")
async def call_typo_checker(request: AnalysisRequest):
    """
    Accepts a sentence, and returns the correction 
    (or an empty string if the sentence is correct). 
    """
    system_prompt = (
        "You are a Japanese typo checker. "
        "Check if the user's Japanese sentence contains obvious typos "
        "(wrong kana, common mistakes), and return your evaluation:\n"
        "- sentence is fine = return 'ok',\n"
        "- obvious typo/miss = return 'typo' (along with a corrected version),\n"
        "- sentence is in japanese but incomprehensible = return 'nonsense',\n"
        "- sentence is not in japanese at all = return 'foreign'."
    )
    response = client.chat.complete(
        model="ministral-8b-latest",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": request.sentence}
        ],
        response_format={
            "type": "json_object",
            "properties": {
                "evaluation": {
                    "type": "string",
                    "enum": ["ok", "typo", "nonsense", "foreign"]
                },
                "correction": {
                    "type": "string",
                    "description": "Corrected version if typo detected, null otherwise",
                    "nullable": True
                }
            },
            "required": ["evaluation", "correction"]
        }
    )
    result = json.loads(response.choices[0].message.content)
    print(result)
    return { **result  }
    # return content

@app.get("/api/health")
async def health_check():
    return {"status": "ok"}

app.mount("/", StaticFiles(directory=front_dir), name="static")
