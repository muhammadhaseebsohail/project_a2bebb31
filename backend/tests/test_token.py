Here's how you might write unit tests for the FastAPI application mentioned earlier:

```python
# necessary imports
from fastapi.testclient import TestClient
from main import app, Item
from pydantic import ValidationError
import pytest

# create test client
client = TestClient(app)

# sample item to use in tests
sample_item = {
    "name": "Test Item",
    "description": "This is a test item",
    "price": 10.0,
    "quantity": 5
}

def test_create_item():
    response = client.post("/items/1", json=sample_item)
    assert response.status_code == 200
    assert response.json() == sample_item

def test_create_existing_item():
    response = client.post("/items/1", json=sample_item)
    assert response.status_code == 400
    assert response.json() == {"detail": "Item already exists"}

def test_read_valid_item():
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json() == sample_item

def test_read_invalid_item():
    response = client.get("/items/nonexistent")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}

def test_item_model_validation():
    # Test with missing fields
    with pytest.raises(ValidationError):
        item = Item(**{"name": "Incomplete Item"})
    
    # Test with wrong types
    with pytest.raises(ValidationError):
        item = Item(**{"name": "Bad Item", "price": "not a number", "quantity": "not a number"})
```
In these tests:

- `test_create_item` checks that you can create an item successfully.
- `test_create_existing_item` checks that the API doesn't allow you to create an item with an existing ID.
- `test_read_valid_item` checks that you can read an existing item.
- `test_read_invalid_item` checks that the API returns the correct error when trying to read a non-existent item.
- `test_item_model_validation` checks that the `Item` model correctly validates the data, raising errors when required fields are missing or when fields are of the wrong type.

Please note that these tests assume that the server is stateless i.e., the data is not stored persistently. In a real-world application, you would probably use a database, and you would need to set up your tests to clean the database before each test.