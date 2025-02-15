from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse

from common.logs import setup_logging
from middleware import process_time_middleware, ErrorMiddleware

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
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    # Если exc.detail уже является словарём, можно вернуть его напрямую.
    # Если это не так, можно обернуть в нужный формат.
    content = exc.detail if isinstance(exc.detail, dict) else {"message": exc.detail}
    return JSONResponse(status_code=exc.status_code, content=content)


@app.get("/")
async def root():
    logger.info("hello world!")
    return {"Hello": "World"}
