index: str = """<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        /* Insert your CSS styles here */
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            min-height: 100vh;
        }

        header,
        main,
        footer {
            padding: 20px;
        }

        header {
            background-color: #333;
            color: #fff;
            text-align: center;
        }

        main {
            flex: 1;
            max-width: 800px;
            margin: 0 auto;
        }

        a {
            color: #007bff;
            text-decoration: none;
        }

        footer {
            background-color: #333;
            color: #fff;
            text-align: center;
            padding: 10px 0;
            position: absolute;
            bottom: 0;
            width: 100%;
        }
    </style>
    <title>Movie API Documentation</title>
</head>

<body>
    <header>
        <h1>Welcome to Movie API Documentation</h1>
    </header>
    <main>
        <section>
            <h2>Using the Movie API</h2>
            <p>This API allows you to perform CRUD operations on movie data.</p>
            <h3>API Base URL:</h3>
            <p>http://localhost:5000</p>
        </section>
        <section>
            <h2>Accessing API Documentation</h2>
            <p>To access the API documentation and test endpoints, go to:</p>
            <p><a href="/docs" target="_blank">Swagger Documentation</a></p>
        </section>
    </main>
    <footer>
        <p>&copy; 2023 Movie API</p>
    </footer>
</body>

</html>
"""
