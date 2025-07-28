import os

from dotenv import load_dotenv

load_dotenv()

# Configurações de ambiente
DEBUG = os.getenv("DEBUG", "true").lower() in ("true", "1")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")  # development, staging, production

# Configurações de servidor
SERVER_HOST = os.getenv("SERVER_HOST", "localhost")
SERVER_PORT = int(os.getenv("APP_PORT", 5000))

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

STOCK_MICROSERVICE_X_API_KEY = os.getenv("STOCK_MICROSERVICE_X_API_KEY")
