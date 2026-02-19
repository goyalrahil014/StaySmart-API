"""
App settings and configuration loader.
"""
from pydantic_settings import BaseSettings
from pydantic import ConfigDict


import os
import sys

def _choose_env_file():
    # Use .env.test if running under pytest or if ENV_FILE is set
    if os.environ.get('ENV_FILE'):
        return os.environ['ENV_FILE']
    if any('pytest' in arg for arg in sys.argv):
        return '.env.test'
    return '.env'

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = ConfigDict(env_file=_choose_env_file())

settings = Settings()
