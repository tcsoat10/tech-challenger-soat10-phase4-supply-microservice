from config.custom_openapi import custom_openapi
from fastapi import FastAPI
from src.adapters.driver.api.v1.middleware.api_key_middleware import ApiKeyMiddleware
from src.adapters.driver.api.v1.middleware.identity_map_middleware import IdentityMapMiddleware
from src.core.containers import Container
from src.adapters.driver.api.v1.middleware.custom_error_middleware import CustomErrorMiddleware
from src.adapters.driver.api.v1.routes.health_check import router as health_check_router
from src.adapters.driver.api.v1.routes.category_routes import router as category_routes
from src.adapters.driver.api.v1.routes.product_routes import router as product_routes

app = FastAPI(title="Tech Challenger SOAT10 - FIAP")

# Inicializando o container de dependências
container = Container()
app.container = container

app.openapi = lambda: custom_openapi(app)

app.add_middleware(CustomErrorMiddleware)
app.add_middleware(ApiKeyMiddleware)
app.add_middleware(IdentityMapMiddleware)

# Adicionando rotas da versão 1
app.include_router(health_check_router, prefix="/api/v1")
app.include_router(category_routes, prefix="/api/v1", tags=["categories"])
app.include_router(product_routes, prefix="/api/v1", tags=["products"])