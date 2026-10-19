from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="Product CRUD API",
    description="FastAPI CRUD application running with Podman",
    version="1.0.0",
)


class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    price: float = Field(gt=0)
    quantity: int = Field(ge=0)


class Product(ProductCreate):
    id: int


# Demo-only in-memory storage. Data is lost when the process restarts.
products: dict[int, Product] = {}
next_id = 1


@app.get("/")
def home():
    return {"message": "Product CRUD API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post(
    "/products",
    response_model=Product,
    status_code=status.HTTP_201_CREATED,
)
def create_product(product: ProductCreate):
    global next_id

    new_product = Product(id=next_id, **product.model_dump())
    products[next_id] = new_product
    next_id += 1
    return new_product


@app.get("/products", response_model=list[Product])
def get_products():
    return list(products.values())


@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int):
    product = products.get(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, product: ProductCreate):
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")

    updated_product = Product(id=product_id, **product.model_dump())
    products[product_id] = updated_product
    return updated_product


@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")

    del products[product_id]
    return {"message": f"Product {product_id} deleted"}
