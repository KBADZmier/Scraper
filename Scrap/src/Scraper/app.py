from fastapi import FastAPI
import asyncio
import aiohttp
import random
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from aiohttp_socks import ProxyConnector
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["GET"], 
    allow_headers=["*"],  
)
print("✅ CORS powinien działać!")
# 🔄 Rotacja User-Agentów
ua = UserAgent()

# 🔌 Proxy (TOR / inne SOCKS5)
PROXY_URL = "socks5://127.0.0.1:9050"

# 📈 Ustawienia scrapingu
RESULTS_TO_FETCH = 10  # Liczba wyników Google
MIN_DELAY = 2
MAX_DELAY = 5

async def fetch(session, url):
    """ Pobiera stronę asynchronicznie przez proxy """
    headers = {"User-Agent": ua.random}
    async with session.get(url, headers=headers) as response:
        return await response.text()

async def scrape_google(query):
    """ Szuka wyników w Google """
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}&num={RESULTS_TO_FETCH}"
    
    connector = ProxyConnector.from_url(PROXY_URL)
    async with aiohttp.ClientSession(connector=connector) as session:
        html = await fetch(session, search_url)
        soup = BeautifulSoup(html, "lxml")

        results = []
        for g in soup.select(".tF2Cxc"):  # Google wynik (może się zmieniać)
            title = g.select_one("h3").text if g.select_one("h3") else "Brak tytułu"
            link = g.select_one("a")["href"] if g.select_one("a") else "Brak linku"
            results.append({"title": title, "link": link})

        return results

@app.get("/search/")
async def search(query: str):
    """ API do wyszukiwania """
    results = await scrape_google(query)
    return {"results": results}

# 🚀 Uruchomienie serwera: `uvicorn app:app --reload`
