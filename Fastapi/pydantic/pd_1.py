import uuid
from enum import Enum
from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field, UUID4, HttpUrl, field_validator, model_validator, computed_field
from typing_extensions import Annotated

class Genre(str, Enum):
    fiction = 'fiction'
    nonfiction = 'nonfiction'
    mystery = 'mystery'
    fantasy = 'fantasy'
    biography = 'biography'
    science_fiction = 'Science Fiction'

class Author(BaseModel):
    name: str
    email: str

class BookPublication(BaseModel):
    pub_id: UUID4 = Field(default_factory=uuid.uuid4)

    title: Annotated[
        str, Field(..., min_length=1, max_length=200, description="Title of the book", examples=["The Great Adventure"])
    ]

    author: Author  # nested model

    genre: Genre = Genre.fiction

    pub_year: Annotated[
        int, Field(..., ge=1450, le=date.today().year, description="Publication year of the book", examples=[2020])
    ]

    pages: Annotated[
        int, Field(..., gt=0, description="Number of pages in the book")
    ]
    
    keywords: Optional[List[str]] = Field(default=[], max_length=10)

    promo_url: Optional[HttpUrl] = None

    # field validator
    @field_validator("title")
    @classmethod
    def transform_title(cls, v: str) -> str:
        return v.title()
    # model validator
    @model_validator(mode="after")
    def check_sci_fi_publication_year(self):
        if self.genre == Genre.science_fiction and self.pub_year < 1818:
            raise ValueError("Science Fiction is considered to have started after 1818.")
        return self
    # computed field
    @computed_field
    @property
    def book_summary(self) -> str:
        return f"'{self.title}' by {self.author.name}, published in {self.pub_year}."

book_data = {
    "title": "a journey through the stars",
    "author": {
        "name": "Dr. Evelyn Reed",
        "email": "e.reed@galaxy.edu"
    },
    "genre": "Science Fiction", 
    "pub_year": 2024,         
    "pages": 350,
    "keywords": ["Space", "Exploration", "AI"], 
    "promo_url": "https://journey-stars.com"
}

try:
    new_book = BookPublication(**book_data)
    
    print("--- Validated Object ---")
    print(new_book)
    
    print("\n--- Summary ---")
    print(f"Summary: {new_book.book_summary}")
    
    print("\n--- JSON Output ---")
    print(new_book.model_dump_json(exclude_unset=True, indent=2))

except ValueError as e:
    print(f"Validation Failed: {e}")