from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from common.logs import setup_logging
from common.middleware import custom_http_exception_handler, process_time_middleware, ErrorMiddleware

app = FastAPI(
    title="Base App"
)
logger = setup_logging()


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


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return await custom_http_exception_handler(request, exc)


@app.get("/")
async def root():
    logger.info("hello world!")
    return {"Hello": "World"}
