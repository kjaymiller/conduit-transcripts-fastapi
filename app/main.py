from typing import Annotated, List

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel


from more_itertools import bucket

from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

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

@app.get("/", response_class=HTMLResponse)
def read_item(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={"request": request})

def ai_stream_response(query:str, results: List[str]):
    print("testing")
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
    
    stream = chain.invoke(topic)
    for i in stream:
        print(i, end="", flush=True)


@app.post("/query_search", response_class=HTMLResponse)
def query_search(request:Request, query: Annotated[str, Form()]):
    
    results = similarity_search(query)
    clean_results = [x[0].page_content.lstrip(". ").lstrip("? ") for x in results]
    ai_stream_response(query, clean_results)
    return templates.TemplateResponse(
        request=request,
        name="loaded_results.html",
        context={
            "results": results,
            "query": query,
        }
    )

@app.post("/search", response_class=HTMLResponse)
def search(request: Request, query: Annotated[str, Form()]):

    return templates.TemplateResponse(
        request=request,
        name="search_results.html",
        context={
            "query": query,
        }
    )