import asyncio
from typing import Annotated, List

from fastapi import FastAPI,Depends
from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import CustomerResponse, CustomerCreate, ProductUpdate
from schemas import ProductCreate, ProductResponse
from database import get_session,init_db
from models import Product, Customer

app = FastAPI()



@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/products",response_model=ProductResponse)
async def create_product(product_data: ProductCreate, db: AsyncSession = Depends(get_session)):
    new_product = Product(
        name = product_data.name,
        price = product_data.price,
        stock = product_data.stock
    )

    db.add(new_product)

    await db.commit()
    await db.refresh(new_product)
    return new_product


@app.get("/products",response_model=list[ProductResponse])
async def get_all_products(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Product).order_by(Product.id))
    products = result.scalars().all()
    return products

@app.post("/customers",response_model=CustomerResponse)
async def create_customer(user_data: CustomerCreate, db: AsyncSession = Depends(get_session)):
    new_customer = Customer(
        name = user_data.name,
        email = user_data.email,
        address = user_data.address,
    )

    db.add(new_customer)
    await db.commit()
    await db.refresh(new_customer)
    return new_customer

@app.get("/customers",response_model=list[CustomerResponse])
async def get_customers(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Customer))
    all_customers = result.scalars().all()
    return all_customers

@app.delete("/products")
async def delete_products(db: AsyncSession = Depends(get_session)):
    await db.execute(delete(Product))
    await db.commit()

@app.patch("/products/{product_id}")
async def update_products(product_id:int, new_data: ProductUpdate, db: AsyncSession = Depends(get_session)):
    updated_data = new_data.model_dump(exclude_unset=True)

    result = await db.execute(
        update(Product)
        .where(Product.id == product_id)
        .values(**updated_data)
    )

    await db.commit()
    product = await db.get(Product,product_id)
    return product

