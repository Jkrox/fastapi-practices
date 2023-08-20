from fastapi import HTTPException
from config.database import session
from models.movie import Movie as MovieModel
from schemas.movie import Movie

from typing import List


class MovieService:
    def __init__(self, db: session) -> None:
        self._db = db

    @property
    def db(self):
        return self._db

    def get_movies(self) -> List[MovieModel]:
        result: List[MovieModel] | None = self._db.query(MovieModel).all()
        if not result:
            raise HTTPException(
                status_code=404, detail="There are no movies in the database."
            )
        return result

    def get_movie(self, id: int) -> MovieModel:
        result: MovieModel | None = (
            self._db.query(MovieModel).filter(MovieModel.id == id).first()
        )
        if not result:
            raise HTTPException(status_code=404, detail="Movie not found.")
        return result

    def get_movies_by_category(self, category: str) -> List[MovieModel]:
        result: List[MovieModel] | None = (
            self._db.query(MovieModel).filter(MovieModel.category == category).all()
        )
        if not result:
            raise HTTPException(status_code=404, detail="Movie not found.")
        return result

    def create_movie(self, movie: Movie) -> None:
        new_movie = MovieModel(**movie.dict())
        self._db.add(new_movie)
        self._db.commit()
        return
