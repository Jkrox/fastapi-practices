from fastapi import Depends, FastAPI, Path, Query, HTTPException, status, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security.http import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import Optional, List
from config.database import base, engine, session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder

from jwt_manager import create_token, validate_token
from dotenv import load_dotenv

import datetime
import os

app = FastAPI()
app.title = "Documentación test1"
app.version = "0.0.1"

base.metadata.create_all(bind=engine)

# Load environment variables from .env file
load_dotenv()

# --------------------------------------------------------------------------------

movies = [
    {
        "id": 1,
        "title": "Avatar",
        "overview": "En un exuberante planeta llamado Pandora viven los Na'vi",
        "year": 2009,
        "rating": 7.8,
        "category": "Acción",
    },
    {
        "id": 2,
        "title": "Avatar 2",
        "overview": "En un exuberante planeta llamado Pandora viven los Na'vi",
        "year": 2019,
        "rating": 9,
        "category": "Acción",
    },
]

# --------------------------------------------------------------------------------


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        auth: HTTPAuthorizationCredentials | None = await super().__call__(request)
        data = validate_token(auth.credentials, os.getenv("KEY"))
        if data["email"] == None and data["email"] != "test@gmail.com":
            raise HTTPException(status_code=403, detail="Invalid crendentials")


# --------------------------------------------------------------------------------


class User(BaseModel):
    email: str = Field(..., min_length=5, max_length=50)
    password: str = Field(..., min_length=5, max_length=50)


# --------------------------------------------------------------------------------


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


# --------------------------------------------------------------------------------


@app.get("/", tags=["Home"])
def hello():
    return HTMLResponse("<h1>Hello World</h1>")


# --------------------------------------------------------------------------------


@app.post("/login", tags=["login"])
def login(user: User):
    if user.email == "test@gmail.com" and user.password == "demokeys12345":
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Login successful",
                "token": create_token(user.dict(), os.getenv("KEY")),
            },
        )


# --------------------------------------------------------------------------------


@app.get(
    "/movies",
    tags=["movies"],
    response_model=List[Movie],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(JWTBearer())],
)
def get_movies() -> List[Movie]:
    db = session()
    result = db.query(MovieModel).all()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


# --------------------------------------------------------------------------------


@app.get(
    "/movies/{id}",
    tags=["movies"],
    response_model=Movie,
    status_code=status.HTTP_200_OK,
)
def get_movie(id: int = Path(ge=1, le=200)) -> Movie:
    db = session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Movie not found.")
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


# --------------------------------------------------------------------------------


@app.get(
    "/movies/",
    tags=["movies"],
    response_model=List[Movie],
    status_code=status.HTTP_200_OK,
)
def get_movies_by_category(
    category: str = Query(None, min_length=3, max_length=15)
) -> List[Movie]:
    db = session()
    result = db.query(MovieModel).filter(MovieModel.category == category).all()
    if not result:
        raise HTTPException(status_code=404, detail="Movie not found.")
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


# --------------------------------------------------------------------------------


@app.post(
    "/movies", tags=["movies"], response_model=dict, status_code=status.HTTP_201_CREATED
)
def create_movie(movie: Movie) -> dict:
    db = session()
    new_movie = MovieModel(**movie.dict())
    db.add(new_movie)
    db.commit()
    movies.append(movie.dict())
    return JSONResponse(content={"message": "Movie created"})


# --------------------------------------------------------------------------------


@app.put(
    "/movies/{id}", tags=["movies"], response_model=dict, status_code=status.HTTP_200_OK
)
def update_movie(id: int, movie: Movie) -> dict:
    db = session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Movie not found.")
    result.title = movie.title
    result.overview = movie.overview
    result.year = movie.year
    result.rating = movie.rating
    result.category = movie.category
    db.commit()
    return JSONResponse(status_code=200, content={"message": "Movie modified."})


# --------------------------------------------------------------------------------


@app.put(
    "/movies/",
    tags=["movies"],
    response_model=List[Movie],
    status_code=status.HTTP_200_OK,
)
def update_movies(ids: List[int], movie: Movie) -> List[Movie]:
    updated_movies = []
    found = False
    for index, item in enumerate(movies):
        if item["id"] in ids:
            found = True
            movies[index] = movie.dict()
            updated_movies.append(movies[index])
        else:
            updated_movies.append(item)
    if not found:
        raise HTTPException(status_code=404, detail="Movie not found.")
    return updated_movies


# --------------------------------------------------------------------------------


@app.delete(
    "/movies/{id}", tags=["movies"], response_model=dict, status_code=status.HTTP_200_OK
)
def delete_movie(id: int) -> dict:
    for movie in movies:
        if movie["id"] == id:
            movies.remove(movie)
            return JSONResponse(content={"message": "Movie deleted."})
    raise HTTPException(status_code=404, detail="Movie not found.")


# --------------------------------------------------------------------------------
# To run the server, try to use the following command:
# uvicorn main:app --reload --port 5000 --host 0.0.0.0
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=5000, reload=True)
