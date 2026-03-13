from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from pydantic import BaseModel

back_dir = Path(__file__).parent
front_dir = back_dir / ".." / "frontend"
app = FastAPI()

# ---
# GET requests

@app.get("/")
async def serve_index():
    return FileResponse(front_dir / "index.html")
@app.get("/typo-checker")
async def serve_index():
    return FileResponse(front_dir / "typo-checker.html")

# 2. validation of the client's request
class AnalysisRequest(BaseModel):
    sentence: str
    # intended_meaning: str
    # tone: str
    # context: str

@app.post("/api/typo-checker")
async def call_typo_checker(request: AnalysisRequest):
    """
    Accepts a sentence, and returns the correction 
    (or an empty string if the sentence is correct). 
    """
    print(f"Received sentence for analysis: {request.sentence}")

    return {
        "status": "success",
        "received_sentence": request.sentence,
        "analysis": "This is a placeholder analysis. The real AI response will go here."
    }

@app.get("/api/health")
async def health_check():
    return {"status": "ok"}

app.mount("/", StaticFiles(directory=front_dir), name="static")
