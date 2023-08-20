from fastapi import APIRouter
from fastapi import Depends, Path, Query, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List
from config.database import session
from middlewares.jwt_bearer import JWTBearer
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from services.movie import MovieService
from schemas.movie import Movie

movie_router = APIRouter()


# --------------------------------------------------------------------------------


@movie_router.get(
    "/movies",
    tags=["movies"],
    response_model=List[Movie],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(JWTBearer())],
)
def get_movies() -> List[Movie]:
    db = session()
    result = MovieService(db).get_movies()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


# --------------------------------------------------------------------------------


@movie_router.get(
    "/movies/{id}",
    tags=["movies"],
    response_model=Movie,
    status_code=status.HTTP_200_OK,
)
def get_movie(id: int = Path(ge=1, le=200)) -> Movie:
    db = session()  # The handler_error middleware must appear here.
    result = MovieService(db).get_movie(id)
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


# --------------------------------------------------------------------------------


@movie_router.get(
    "/movies/",
    tags=["movies"],
    response_model=List[Movie],
    status_code=status.HTTP_200_OK,
)
def get_movies_by_category(
    category: str = Query(None, min_length=3, max_length=15)
) -> List[Movie]:
    db = session()
    result = MovieService(db).get_movies_by_category(category)
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


# --------------------------------------------------------------------------------


@movie_router.post(
    "/movies", tags=["movies"], response_model=dict, status_code=status.HTTP_201_CREATED
)
def create_movie(movie: Movie) -> dict:
    db = session()
    MovieService(db).create_movie(movie)
    return JSONResponse(content={"message": "Movie created"})


# --------------------------------------------------------------------------------


@movie_router.put(
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


@movie_router.put(
    "/movies/",
    tags=["movies"],
    response_model=List[Movie],
    status_code=status.HTTP_200_OK,
)
def update_movies(ids: List[int], movie: Movie) -> List[Movie]:
    db = session()
    updated_movies = []
    found = False

    for movie_id in ids:
        result = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
        if result:
            found = True
            result.title = movie.title
            result.overview = movie.overview
            result.year = movie.year
            result.rating = movie.rating
            result.category = movie.category
            updated_movies.append(result)
        else:
            raise HTTPException(
                status_code=404, detail="Movie with ID {movie_id} not found.}"
            )

    if not found:
        raise HTTPException(status_code=404, detail="Movie not found.")

    return JSONResponse(status_code=200, content=jsonable_encoder(updated_movies))


# --------------------------------------------------------------------------------


@movie_router.delete(
    "/movies/{id}", tags=["movies"], response_model=dict, status_code=status.HTTP_200_OK
)
def delete_movie(id: int) -> dict:
    db = session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Movie not found.")

    db.delete(result)
    db.commit()
    return JSONResponse(content={"message": "Movie deleted."})
