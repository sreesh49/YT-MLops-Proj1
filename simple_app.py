# simple_app.py
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import os

app = FastAPI()

# Simple template setup
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def home(request: Request):
    try:
        return templates.TemplateResponse("vehicledata.html", {"request": request})
    except Exception as e:
        return HTMLResponse(f"Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)