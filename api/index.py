# filename: main.py

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Welcome to Wikipedia Outline API. Try /api/outline?country=India"}

@app.get("/api/outline")
def get_outline(country: str = Query(...)):
    url = f"https://en.wikipedia.org/wiki/{country.replace(' ', '_')}"
    response = requests.get(url)
    
    if response.status_code != 200:
        return {"error": "Country not found on Wikipedia"}
    
    soup = BeautifulSoup(response.text, "html.parser")
    headings = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])
    
    md = ["## Contents"]
    for h in headings:
        level = int(h.name[1])
        text = h.get_text(strip=True)
        md.append(f"{'#' * level} {text}")
    
    return {"markdown": "\n".join(md)}

