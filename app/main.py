import os
import models.audio2text as audio2text
from model_proccessors import MODEL_MAP, health_check
from fastapi import FastAPI, File, UploadFile, Request
from typing import Optional
from pathlib import Path
import uvicorn
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from contextlib import asynccontextmanager
from dataclasses import dataclass
from functools import partial
from concurrent.futures import ProcessPoolExecutor
import time
import asyncio
import uuid
from collections import defaultdict
from fastapi.security import OAuth2PasswordBearer

# <<< START ASYNC QUEUE
class Item:
    id: str
    name: str
    args = {}

    def __init__(self, id, name, args = {}):
        self.id = id
        self.name = name
        self.args = args
    
    def to_dict(self):
        return jsonable_encoder({
            "id": self.id,
            "name": self.name,
            "args": self.args
        })

        


def fn_runner(item: Item):
    return  MODEL_MAP.get(item.name)(item.args)

async def process_requests(q: asyncio.Queue, pool: ProcessPoolExecutor):
    while True:
        item = await q.get()  # Get a request from the queue
        loop = asyncio.get_running_loop()
        fake_db[item.id]["status"] = "Processing"
        r = await loop.run_in_executor(pool, fn_runner, item)
        q.task_done()  # tell the queue that the processing on the task is completed
        fake_db[item.id]["status"] = "Complete"
        fake_db[item.id]["runtime"] = time.time() - fake_db[item.id]["start_time"]
        fake_db[item.id]["data"] = r
        print('job finished: ', item.id)


@asynccontextmanager
async def lifespan(app: FastAPI):
    q = asyncio.Queue()  # note that asyncio.Queue() is not thread safe
    pool = ProcessPoolExecutor()
    asyncio.create_task(process_requests(q, pool))  # Start the requests processing task
    yield {"q": q, "pool": pool}
    pool.shutdown()  # free any resources that the pool is using when the currently pending futures are done executing


fake_db = defaultdict(str)

def add_to_queue(request, name: str, args={}):
    print('adding to queue', name, args)
    item_id = str(uuid.uuid4())
    item = Item(item_id, name, args)
    request.state.q.put_nowait(item)  # Add request to the queue
    start_time = time.time()
    fake_db[item_id] = {"status": "Waiting", "start_time": start_time }
    return item_id

# >>> END ASYNC QUEUE


app = FastAPI(lifespan=lifespan)

# API ROUTES OUTSIDE OF INVOKE
@app.get("/")
def health_check_api():
    return health_check()

@app.get("/translate-demo")
async def translate_demo_api(request: Request):
    return add_to_queue(request, 'translate_audio_demo') 

@app.get("/translate-text")
async def translate_text_api(request: Request, eg_t: str):
    return add_to_queue(request, 'translate_text', {"eg_t": eg_t})

@app.post("/translate-audio")
async def translate_audio_upload_api(request: Request, audio_file: UploadFile = File(...)):
    return add_to_queue(request, 'translate_audio_upload', {"audio_file": audio_file})

@app.get("/status")
async def check_status(id: str):
    if id in fake_db:
        return fake_db[id]
    else:
        return JSONResponse("Process ID Not Found", status_code=404)

# AWS INVOCATION ROUTE 
# @app.post('/invocations')
# async def invoke(audio_file: UploadFile | None = None, route: str = "None", arabic_text: str = ""):
#     if audio_file is not None:
#         return translate_audio_upload(audio_file)
#     elif route == 'translate_text' and len(arabic_text) > 0:
#         return translate_text(arabic_text)
#     elif route == 'translate_demo':  
#         return translate_demo()
#     else:
#       return health_check()
    


if __name__ == "__main__":
    # config = uvicorn.Config("main:app", port=8000, log_level="info")
    # server = uvicorn.Server(config)
    uvicorn.run(app)