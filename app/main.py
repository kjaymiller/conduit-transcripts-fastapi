import os
import logging
import dotenv
from contextlib import asynccontextmanager
import uuid
from markdown import markdown

from typing import Annotated

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, StreamingResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from pydantic import BaseModel


from more_itertools import bucket
from ollama import Client as OllamaClient

from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

import db.pg.crud as pg
from db.search import similarity_search
from db.redis import redis_connection as redis

dotenv.load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME", "llama3")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Context manager to ensure that the Llama3 model is downloaded before the app starts"""
    ollama = OllamaClient(host=os.getenv("OLLAMA_HOST", "http://localhost:11434"))
    if f"{MODEL_NAME}:latest" not in ollama.list()['models']:
        logging.info(f"Downloading {MODEL_NAME} model")
        ollama.pull(MODEL_NAME)
    yield

app = FastAPI(lifespan=lifespan)

class APIRequest(BaseModel):
    query: str

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def strip_text(text:str):
    return text.lstrip(". ").lstrip("? ")

templates.env.filters["strip_text"] = strip_text

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={"request": request})


@app.get("/enable_ai", response_class=RedirectResponse)
async def enable_ai(request: Request):
    response = RedirectResponse(
        url="/",
        status_code=302,
    )
    response.set_cookie(key="enable_ai", value=True)
    return response

    return response

@app.get("/disable_ai", response_class=RedirectResponse)
async def disable_ai(request: Request):

    response = RedirectResponse(
        url="/",
        status_code=302,
    )
    response.set_cookie(key="enable_ai", value=False)
    return response

@app.get("/old", response_class=HTMLResponse)
def old_home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={"request": request, "no_ai": True})

@app.get("/episodes/", response_class=HTMLResponse)
def all_episodes(request: Request): 
    episodes = sorted(pg.all_episodes(), key=lambda x: int(x.title.split(":")[0]), reverse=True)
    return templates.TemplateResponse("all_episodes.html", {"request": request, "episodes": episodes})

@app.get("/episode_by_title", response_class=HTMLResponse)
def episode_by_title(request: Request, title: str):
    episode = pg.get_episode_by_title(title)
    episode_content = markdown(episode.content)
    return templates.TemplateResponse("episode.html", {"request": request, "episode": episode , "episode_content": episode_content})

@app.get("/episode/{episode_id}", response_class=HTMLResponse)
def episode(request: Request, episode_id: int):
    episode = pg.get_episode_by_id(episode_id)
    episode_content = markdown(episode.content)
    return templates.TemplateResponse("episode.html", {"request": request, "episode": episode, "episode_content": episode_content})

@app.get("/ai_query_search/{query_id}")
async def ai_query_search(query_id: str):
    
    def ai_stream_response(query_id:str):
        
        job = redis.hgetall(query_id)
        if redis.hget(query_id, "status") == "not started":
            llm = ChatOllama(model=MODEL_NAME,base_url=os.getenv("OLLAMA_HOST", "http://localhost:11434"))
            prompt = ChatPromptTemplate.from_template("""
                    Offer supportive advice for the question {query} with supporting quotes from Kathy and Jay who say 
                    
                    Quotes: "{docs}".

                    Only use quotes mentioned.
                    If no quotes  - Say so and stop generating a response.                                                                                                                                                           
                    Make responses about 1000 characters
            """)

            chain = prompt | llm | StrOutputParser()
            topic = {"query": job["query"], "docs": job["docs"]}
            
            response = ""
            for content in chain.stream(topic):
                response += content 
                yield f"data:{content} \n\n"
            
            redis.hset(query_id, "response", markdown(response).replace("\n", ""))
            redis.hset(query_id, "status", "completed")
        
        print(response)
        yield f'data: Generation Complete: Response: {redis.hget(query_id, "response")}\n\n'

        print(redis.hgetall(query_id))
        yield 'data:Terminate Connection\n\n'

    return StreamingResponse(ai_stream_response(query_id), media_type="text/event-stream")


@app.post("/ai_search", response_class=HTMLResponse)
async def ai_search(
    request: Request,
    query: Annotated[str, Form()],
):
    query_id = str(uuid.uuid4())
    search_results = similarity_search(query)
    results = bucket(search_results, lambda x: x[0].metadata['title'])
    docs = [x[0].page_content.lstrip(". ").lstrip("? ") for x in search_results]
    rds_values = {"query": query, "status": "not started", "docs": "\n".join(docs)}
    redis.hset(query_id, mapping=rds_values)


    return templates.TemplateResponse(
        request=request,
        name="ai_search_results.html",
        context={
            "query_id": query_id,
            "query": query,
            "results": results,
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

resource = Resource(attributes={
    "service.name": "conduit-ai-transcription"
})

if os.getenv("telemetry", False):
    traceProvider = TracerProvider(resource=resource)
    otlp_exporter = OTLPSpanExporter(endpoint="jaeger:4317", insecure=True)
    span_processor = BatchSpanProcessor(otlp_exporter)
    traceProvider.add_span_processor(span_processor)
    trace.set_tracer_provider(traceProvider)
    FastAPIInstrumentor.instrument_app(app)