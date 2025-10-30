from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Annotated, List

app = FastAPI()

class item(BaseModel):
    name: Annotated[str, Field(..., title="Item Name",min_length=1, max_length=30)]
    description: Annotated[str, Field(..., title="Item description", max_length=50)]
    price: float = Field(..., gt=0, description="The price must be greater than zero")
    tags: List[str] | None = Field(default=[], title="Tags for the item")

fake_item_db : Dict[str, item] = {
    "item1" : item(
        name="Sample Item",
        description="This is a sample item",
        price=10.5,
        tags=["sample", "item"]
    ),
    "item2" : item(
        name="Another Item",
        description="This is another item",
        price=20.0,
        tags=["another", "item"]
    )
}

@app.get("/")
async def read_item():
    return{"respnse":"hello welcome"}

@app.put("/items/{item_id}", response_model=item)
async def update_item(item_id: str, update_item: item):
    if item_id not in fake_item_db:
        raise HTTPException(status_code=404, detail="Item not found")   
    fake_item_db[item_id] = update_item
    return update_item

@app.delete("/items/{item_id}")
async def delete_item(item_id: str):
    if item_id not in fake_item_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del fake_item_db[item_id]
    return {"detail": "Item deleted successfully"}