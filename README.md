# FastAPI Movie API

This is a small REST API built with FastAPI that provides information about movies.

## Features

- Get a list of all movies.
- Get details about a specific movie.
- Add a new movie.
- Update an existing movie.
- Delete a movie.

## Getting Started

1. Clone the repository
2. Install the dependencies with `pip install -r requirements.txt`
3. Start the server with `uvicorn main:app --reload`
4. Navigate to `http://localhost:8000/docs` to view the Swagger documentation

## API Endpoints

### GET /movies

Returns a list of all movies.

### GET /movies/{id}

Returns details about a specific movie.

### POST /movies

Adds a new movie to the database.

### PUT /movies/{id}

Updates an existing movie.

### DELETE /movies/{id}

Deletes a movie from the database.

## Technologies Used

- Python
- FastAPI
- SQLAlchemy
- SQLite
