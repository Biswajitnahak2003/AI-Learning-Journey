from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List, Annotated

app = FastAPI()

class item(BaseModel):
    name: Annotated[str, Field(..., title="Item Name",min_length=1, max_length=30)]
    description: Annotated[str, Field(..., title="Item description", max_length=50)]
    price: float = Field(..., gt=0, description="The price must be greater than zero")
    tags: List[str] | None = Field(default=[], title="Tags for the item")

fake_item_db : List[item] = []

@app.get("/")
async def read_root():
    return {"Hello": "welcome to the item store"}

@app.post("/item")
async def create_item(item: item):
    fake_item_db.append(item)
    return item

@app.get("/items", response_model=List[item])
async def get_items():
    return fake_item_db