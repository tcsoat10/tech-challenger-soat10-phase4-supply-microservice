from datetime import datetime
from fastapi import status
import pytest

from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("SUPPLY_MICROSERVICE_X_API_KEY")

from src.core.exceptions.utils import ErrorCode
from tests.factories.category_factory import CategoryFactory
from tests.factories.product_factory import ProductFactory


@pytest.mark.parametrize("payload", [
    {"name": "Coca-Cola", "description": "Soft drink", "price": 6.99, "category_id": None},
    {"name": "Big Mac", "description": "Fast food burger", "price": 20.99, "category_id": None},
])
def test_create_product_success(client, db_session, payload):
    category = CategoryFactory()
    payload["category_id"] = category.id

    response = client.post("/api/v1/products", json=payload, permissions=[], headers={"x-api-key": api_key})

    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()

    assert "id" in data
    assert data["name"] == payload["name"]
    assert data["description"] == payload["description"]
    assert data["price"] == payload["price"]
    assert data["category"]["id"] == category.id
    assert data["category"]["name"] == category.name


def test_create_product_duplicate_name_and_return_error(client, db_session):
    category = CategoryFactory()
    ProductFactory(name="Coca-Cola", category=category)

    payload = {
        "name": "Coca-Cola",
        "description": "Soft drink",
        "price": 6.99,
        "category_id": category.id,
    }

    response = client.post("/api/v1/products", json=payload, permissions=[], headers={"x-api-key": api_key})

    assert response.status_code == status.HTTP_409_CONFLICT

    data = response.json()

    assert data == {
        'detail': {
            'code': str(ErrorCode.DUPLICATED_ENTITY),
            'message': 'Product already exists.',
            'details': None,
        }
    }

def test_reactivate_product_and_return_success(client, db_session):
    category = CategoryFactory(name="Drinks")
    ProductFactory(name="Coca-Cola", category=category, inactivated_at=datetime.now())

    payload = {
        "name": "Coca-Cola",
        "description": "Soft drink",
        "price": 6.99,
        "category_id": category.id,
    }

    response = client.post("/api/v1/products", json=payload, permissions=[], headers={"x-api-key": api_key})

    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()

    assert "id" in data
    assert data["name"] == payload["name"]
    assert data["description"] == payload["description"]
    assert data["price"] == payload["price"]
    assert data["category"]["id"] == category.id
    assert data["category"]["name"] == category.name


def test_get_product_by_name_and_return_success(client):
    category1 = CategoryFactory(name="Drinks")
    category2 = CategoryFactory(name="Fast food")
    ProductFactory(
        name="Coca-Cola",
        description="Soft drink",
        price=6.99,
        category=category1
    )
    ProductFactory(
        name="Big Mac",
        description="Fast food burger",
        price=20.99,
        category=category2
    )

    response = client.get("/api/v1/products/Big Mac/name", permissions=[], headers={"x-api-key": api_key})

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "id" in data
    assert data["name"] == "Big Mac"
    assert data["description"] == "Fast food burger"
    assert data["price"] == 20.99
    assert data["category"]["id"] == category2.id
    assert data["category"]["name"] == category2.name

def test_get_product_by_id_and_return_success(client):
    category1 = CategoryFactory(name="Drinks")
    category2 = CategoryFactory(name="Fast food")
    product1 = ProductFactory(
        name="Coca-Cola",
        description="Soft drink",
        price=6.99,
        category=category1
    )
    ProductFactory(
        name="Big Mac",
        description="Fast food burger",
        price=20.99,
        category=category2
    )
    
    response = client.get(f"/api/v1/products/{product1.id}/id", permissions=[], headers={"x-api-key": api_key})

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "id" in data
    assert data["name"] == "Coca-Cola"
    assert data["description"] == "Soft drink"
    assert data["price"] == 6.99
    assert data["category"]["id"] == category1.id
    assert data["category"]["name"] == category1.name

def test_get_all_products_return_success(client):
    category1 = CategoryFactory(name="Drinks")
    category2 = CategoryFactory(name="Fast food")
    product1 = ProductFactory(
        name="Coca-Cola",
        description="Soft drink",
        price=6.99,
        category=category1
    )
    product2 = ProductFactory(
        name="Big Mac",
        description="Fast food burger",
        price=20.99,
        category=category2
    )
    
    response = client.get("/api/v1/products", permissions=[], headers={"x-api-key": api_key})

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data == [
        {
            "id": product1.id,
            "name": product1.name,
            "description": product1.description,
            "category": {
                "id": product1.category.id,
                "name": product1.category.name,
                "description": product1.category.description,
            },                
            "price": product1.price,
        },
        {
            "id": product2.id,
            "name": product2.name,
            "description": product2.description,
            "category": {
                "id": product2.category.id,
                "name": product2.category.name,
                "description": product2.category.description,
            },
            "price": product2.price,
        },
    ]


def test_update_product_and_return_success(client):
    category = CategoryFactory(name="Fast food")
    category2 = CategoryFactory(name="Burgers")
    
    product = ProductFactory(
        name="Big Mac",
        description="Fast food burger",
        price=20.99,
        category=category
    )
    
    payload = {
        "id": 1,
        "name": "Big Mac - updated",
        "description": "Fast food burger - updated",
        "price": 28.99,
        "category_id": category2.id,
    }

    response = client.put(
        f"/api/v1/products/{product.id}",
        json=payload,
        permissions=[],
        headers={"x-api-key": api_key}
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data == {
        "id": product.id,
        "name": "Big Mac - updated",
        "description": "Fast food burger - updated",
        "price": 28.99,
        "category": {
            "id": category2.id,
            "name": category2.name,
            "description": category2.description,
        },
    }

def test_delete_category_and_return_success(client):
    category1 = CategoryFactory(name="Drinks")
    category2 = CategoryFactory(name="Fast food")
    product1 = ProductFactory(name="Coca-Cola", category=category1)
    product2 = ProductFactory(name="Big Mac", category=category2)

    response = client.delete(f"/api/v1/products/{product1.id}", permissions=[], headers={"x-api-key": api_key})
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = client.get("/api/v1/products", permissions=[], headers={"x-api-key": api_key})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert data == [{
        "id": product2.id,
        "name": product2.name,
        "description": product2.description,
        "price": product2.price,
        "category": {
            "id": product2.category.id,
            "name": product2.category.name,
            "description": product2.category.description,
        },
    }]
