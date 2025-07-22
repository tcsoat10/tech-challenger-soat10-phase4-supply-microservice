from dependency_injector import containers, providers

from config.database import get_db
from src.core.shared.identity_map import IdentityMap
from src.adapters.driver.api.v1.controllers.category_controller import CategoryController
from src.adapters.driven.repositories.category_repository import CategoryRepository
from src.adapters.driver.api.v1.controllers.product_controller import ProductController
from src.adapters.driven.repositories.product_repository import ProductRepository



class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(modules=[
        "src.adapters.driver.api.v1.controllers.category_controller",
        "src.adapters.driver.api.v1.routes.category_routes",
        "src.adapters.driver.api.v1.controllers.product_controller",
        "src.adapters.driver.api.v1.routes.product_routes"
    ])
    
    identity_map = providers.Singleton(IdentityMap)

    db_session = providers.Resource(get_db)

    category_gateway = providers.Factory(
        CategoryRepository,
        db_session=db_session
    )

    category_controller = providers.Factory(
        CategoryController,
        category_gateway=category_gateway
    )

    product_gateway = providers.Factory(ProductRepository, db_session=db_session)
    product_controller = providers.Factory(
        ProductController, product_gateway=product_gateway, category_gateway=category_gateway
    )
