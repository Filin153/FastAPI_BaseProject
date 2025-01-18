from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from logs import logger
from middleware import process_time_middleware, ErrorMiddleware

app = FastAPI(
    title="Base App"
)

@app.on_event("startup")
async def startup():
    logger.info("Start up!")

@app.on_event("shutdown")
async def shutdown():
    logger.info("Shutdown!")

app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_methods=['*'],
                   allow_headers=["*"],
                   allow_credentials=True, )

app.add_middleware(ErrorMiddleware)


@app.middleware('http')
async def process_time(request: Request, call_next):
    return await process_time_middleware(request, call_next)


@app.get("/")
async def root():
    logger.info("hello world!")
    return {"Hello": "World"}
