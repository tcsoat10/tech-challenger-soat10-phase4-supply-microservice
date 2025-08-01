from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from dependency_injector.wiring import inject, Provide

from src.adapters.driver.api.v1.controllers.product_controller import ProductController
#from src.constants.permissions import ProductPermissions
from src.core.auth.dependencies import get_current_user
from src.core.domain.dtos.product.update_product_dto import UpdateProductDTO
from src.core.domain.dtos.product.create_product_dto import CreateProductDTO
from src.core.domain.dtos.product.product_dto import ProductDTO
from src.core.containers import Container


router = APIRouter()


@router.post(
    "/products",
    response_model=ProductDTO,
    status_code=status.HTTP_201_CREATED,
)
@inject
def create_product(
    dto: CreateProductDTO,
    controller: ProductController = Depends(Provide[Container.product_controller]),
):
    return controller.create_product(dto)

@router.get(
    "/products/{product_name}/name",
    response_model=ProductDTO, status_code=status.HTTP_200_OK,
)
@inject
def get_product_by_name(
    product_name: str,
    controller: ProductController = Depends(Provide[Container.product_controller]),
):
    return controller.get_product_by_name(name=product_name)

@router.get(
    "/categories/{category_name}/products",
    response_model=list[ProductDTO],
    status_code=status.HTTP_200_OK,
)
@inject
def get_products_by_category_name(
    category_name: str,
    controller: ProductController = Depends(Provide[Container.product_controller]),
):
    return controller.get_all_products(categories=[category_name])

@router.get(
    "/products/{product_id}/id",
    response_model=ProductDTO,
    status_code=status.HTTP_200_OK,
)
@inject
def get_product_by_id(
    product_id: int,
    controller: ProductController = Depends(Provide[Container.product_controller]),
):
    return controller.get_product_by_id(product_id=product_id)

@router.get(
    "/products",
    response_model=list[ProductDTO],
    status_code=status.HTTP_200_OK,
)
@inject
def get_all_products(
    include_deleted: Optional[bool] = Query(False),
    categories: Optional[list[str]] = Query(None),
    controller: ProductController = Depends(Provide[Container.product_controller]),
):
    return controller.get_all_products(categories=categories, include_deleted=include_deleted)

@router.put(
    "/products/{product_id}",
    response_model=ProductDTO,
    status_code=status.HTTP_200_OK,
)
@inject
def update_product(
    product_id: int,
    dto: UpdateProductDTO,
    controller: ProductController = Depends(Provide[Container.product_controller]),
):
    return controller.update_product(product_id, dto)

@router.delete(
    "/products/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
@inject
def delete_product(product_id: int, controller: ProductController = Depends(Provide[Container.product_controller])):
    controller.delete_product(product_id)
