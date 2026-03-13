from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from pydantic import BaseModel

back_dir = Path(__file__).parent
front_dir = back_dir / ".." / "frontend"
app = FastAPI()
app.mount("/", StaticFiles(directory=front_dir), name="static")

# ---
# GET requests

@app.get("/")
async def serve_index():
    return FileResponse(front_dir / "index.html")



# 2. validation of the client's request
class AnalysisRequest(BaseModel):
    sentence: str
    intended_meaning: str
    tone: str
    context: str

@app.post("/api/full_analysis")
async def full_analysis(request: AnalysisRequest):
    """
    Receives sentence, context, intended meaning, and tone.
    Responds with a full, structured AI analysis.
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
