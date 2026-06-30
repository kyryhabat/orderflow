from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, EmailStr


#Схема продуктов
class BaseProduct(BaseModel):
    name: str
    price: float
    stock: int


class ProductUpdate(BaseModel):

    name: str | None
    price: float | None
    stock: int | None
class ProductCreate(BaseProduct):
    pass



class ProductResponse(BaseProduct):

    id: int

    model_config = ConfigDict(
        from_attributes=True
    )

 #Схема Пользователя
class Customer(BaseModel):
    name:str
    email: EmailStr
    address: str | None

class CustomerCreate(Customer):
    pass

class CustomerResponse(Customer):
    id: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )



