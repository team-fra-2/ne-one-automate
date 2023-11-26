import logging
from contextlib import asynccontextmanager

from dotenv import dotenv_values
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient

from database import init_database
from oidc_token_manager import OIDCTokenManager
from routes import router

# get root logger
logging.getLogger().setLevel(logging.INFO)  # choose your level here
handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)
logging.getLogger().addHandler(handler)

logger = logging.getLogger(__name__)

if (config := dotenv_values(".env")) == {}:
    logger.info("No .env file found")
    import config


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.mongodb_client = MongoClient(config.mongo_db_url)
    app.database = app.mongodb_client[config.mongo_db_database]
    init_database(app.database, reset=False)
    yield
    app.mongodb_client.close()


app = FastAPI(
    title="ne-one automate",
    summary="ONE Record Rule Engine",
    description="ne-one automate is a rule engine to automate the approval process of ONE Record ChangeRequests",
    version="0.0.1",
    license_info={"name": "MIT License", "url": "https://mit-license.org/"},
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

token_manager = OIDCTokenManager(
    token_url=config.access_token_url,
    client_id=config.client_id,
    client_secret=config.client_secret,
    scope=None,
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, workers=1)
