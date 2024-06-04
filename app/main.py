from time import sleep
import asyncio
import json
from typing import Annotated, List

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel


from more_itertools import bucket

from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

import app.db.pg.crud as pg
from app.db.search import similarity_search

app = FastAPI()

class APIRequest(BaseModel):
    query: str

def bucket_results(results):
    """Group search results by episode title and url."""
    grouped_results = bucket(results, lambda x: (x[0].metadata['title'], x[0].metadata['url']))
    keys = list(grouped_results)

    for key in keys:
        key_results = grouped_results[key]

    yield key, key_results

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def strip_text(text:str):
    return text.lstrip(". ").lstrip("? ")

templates.env.filters["strip_text"] = strip_text

@app.get("/", response_class=HTMLResponse)
def read_item(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={"request": request})

@app.get("/episodes/", response_class=HTMLResponse)
def all_episodes(request: Request): 
    episodes = sorted(pg.all_episodes(), key=lambda x: int(x.title.split(":")[0]), reverse=True)
    return templates.TemplateResponse("all_episodes.html", {"request": request, "episodes": episodes})

@app.get("/episode_by_title", response_class=HTMLResponse)
def episode_by_title(request: Request, title: str):
    episode = pg.get_episode_by_title(title)
    return templates.TemplateResponse("episode.html", {"request": request, "episode": episode})

@app.get("/episode/{episode_id}", response_class=HTMLResponse)
def episode(request: Request, episode_id: int):
    episode = pg.get_episode_by_id(episode_id)
    return templates.TemplateResponse("episode.html", {"request": request, "episode": episode})

@app.get("/ai_query_search")
async def ai_query_search():
    
    def ai_stream_response(query:str, results: List[str]):
        llm = ChatOllama(model="llama3")
        prompt = ChatPromptTemplate.from_template("""
                Offer supportive advice for the question {query} with supporting quotes from 
                "{docs}".

                If there are no documents to quote, say "I don't have any information on that."

                Mention the quote you're pulling from                                                                     
                Don't include quotes from other sources
                make responses about 1000 characters
        """)    

        chain = prompt | llm | StrOutputParser()
        topic = {"query": query, "docs": "/n".join(results)}
        
        for content in chain.stream(topic):
            yield content

    async def stream_test():
        for i in range(10):
            yield json.dumps({"data": f"Hello {i}"})
            await asyncio.sleep(1)

    # _results = similarity_search(query)
    # results = bucket(_results, lambda x: x[0].metadata['title'])
    # clean_results = [x[0].page_content.lstrip(". ").lstrip("? ") for x in _results]
    
    # return StreamingResponse(ai_stream_response(query, clean_results))
    return StreamingResponse(stream_test(), media_type="text/event-stream")

@app.post("/ai_search", response_class=HTMLResponse)
async def ai_search(request: Request, query: Annotated[str, Form()]):

    return templates.TemplateResponse(
        request=request,
        name="ai_search_results.html",
        context={
            "query": query,
        }
    )

@app.post("/search", response_class=HTMLResponse)
def search(request: Request, query: Annotated[str, Form()]):
    """Standard Similary Search"""
    results = bucket(similarity_search(query), lambda x: x[0].metadata['title'])

    return templates.TemplateResponse(
        request=request,
        name="search_results.html",
        context={
            "query": query,
            "results": results,
        }
    )