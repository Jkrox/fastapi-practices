from pydantic import BaseModel, Field
from typing import Optional

import datetime


class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(..., min_length=1, max_length=25)
    overview: str = Field(min_length=15, max_length=150)
    year: int = Field(ge=2000, le=datetime.datetime.now().year)
    rating: float = Field(ge=1, le=10)
    category: str = Field(..., min_length=3, max_length=15)

    class Config:
        schema_extra = {
            "example": {
                "title": "Película: ",
                "overview": "Descripción de la película: .",
                "year": 2004,
                "rating": 9.3,
                "category": "Drama",
            },
            "description": "This is an example of a movie object that can be used in the API.",
            "externalDocs": {
                "description": "More information about movies",
                "url": "https://en.wikipedia.org/wiki/List_of_films_considered_the_best",
            },
        }
