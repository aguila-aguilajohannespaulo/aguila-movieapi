from flask import Flask, request, jsonify, render_template
import sqlite3
import os

app = Flask(__name__)
DATABASE = "database.db"
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            year INTEGER NOT NULL,
            genre TEXT NOT NULL
        )
    """)

    count = conn.execute(
        "SELECT COUNT(*) FROM movies"
    ).fetchone()[0]

    if count == 0:
        movies = [
            ("Captain Philippines: The Last Avenger", 1942, "Action"),
            ("The Fantastic Duo: Last Steps", 1964, "Action"),
            ("Captain DC", 1995, "Drama"),
            ("Iron Woman", 2008, "Romance"),
            ("Iron Woman 2", 2010, "Adventure"),
            ("TheDoor", 2023, "Horror"),
            ("The Amazing WonderMan", 2020, "Comedy"),
            ("White Window", 2024, "Science Fiction"),
            ("The Team: Endless Fight", 2017, "Action"),
            ("The Team: Last Gain", 2019, "Drama"),
            ("Homeless Mystery: The Multiverse of Crazy", 2022, "Crime"),
            ("Forever", 2021, "Romance"),
            ("Germ-Man and the Soap: Neuronmania", 2018, "Fantasy"),
            ("Alivepool and Deadpool", 2023, "Adventure"),
            ("SunnyZaps", 2024, "Comedy")
        ]

        conn.executemany(
            """
            INSERT INTO movies (title, year, genre)
            VALUES (?, ?, ?)
            """,
            movies
        )

    conn.commit()
    conn.close()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/movies", methods=["GET"])
def get_movies():
    conn = get_db_connection()
    movies = conn.execute(
        "SELECT * FROM movies ORDER BY id DESC"
    ).fetchall()
    conn.close()
    return jsonify([
        dict(movie) for movie in movies
    ]), 200

@app.route("/movies/<int:movie_id>", methods=["GET"])
def get_movie(movie_id):
    conn = get_db_connection()
    movie = conn.execute(
        "SELECT * FROM movies WHERE id = ?",
        (movie_id,)
    ).fetchone()
    conn.close()
    if movie is None:
        return jsonify({
            "error": "Movie not found"
        }), 404
    return jsonify(dict(movie)), 200

@app.route("/movies", methods=["POST"])
def create_movie():
    data = request.get_json()
    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400
    required_fields = ["title", "year", "genre"]

    for field in required_fields:
        if field not in data or data[field] in ("", None):
            return jsonify({
                "error": f"Missing required field: {field}"
            }), 400

    conn = get_db_connection()
    cursor = conn.execute(
        """
        INSERT INTO movies (title, year, genre)
        VALUES (?, ?, ?)
        """,
        (
            data["title"],
            data["year"],
            data["genre"]
        )
    )

    conn.commit()
    movie = conn.execute(
        "SELECT * FROM movies WHERE id = ?",
        (cursor.lastrowid,)
    ).fetchone()
    conn.close()
    return jsonify(dict(movie)), 201
@app.route("/movies/<int:movie_id>", methods=["PUT"])
def update_movie(movie_id):
    data = request.get_json()
    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400
    required_fields = ["title", "year", "genre"]
    for field in required_fields:
        if field not in data or data[field] in ("", None):
            return jsonify({
                "error": f"Missing required field: {field}"
            }), 400

    conn = get_db_connection()
    movie = conn.execute(
        "SELECT * FROM movies WHERE id = ?",
        (movie_id,)
    ).fetchone()
    if movie is None:
        conn.close()
        return jsonify({
            "error": "Movie not found"
        }), 404

    conn.execute(
        """
        UPDATE movies
        SET title = ?, year = ?, genre = ?
        WHERE id = ?
        """,
        (
            data["title"],
            data["year"],
            data["genre"],
            movie_id
        )
    )

    conn.commit()
    updated_movie = conn.execute(
        "SELECT * FROM movies WHERE id = ?",
        (movie_id,)
    ).fetchone()
    conn.close()
    return jsonify(dict(updated_movie)), 200

@app.route("/movies/<int:movie_id>", methods=["DELETE"])
def delete_movie(movie_id):
    conn = get_db_connection()
    movie = conn.execute(
        "SELECT * FROM movies WHERE id = ?",
        (movie_id,)
    ).fetchone()
    if movie is None:
        conn.close()
        return jsonify({
            "error": "Movie not found"
        }), 404
    conn.execute(
        "DELETE FROM movies WHERE id = ?",
        (movie_id,)
    )
    conn.commit()
    conn.close()
    return jsonify({
        "message": "Movie deleted successfully"
    }), 200

if __name__ == "__main__":
    init_db()
    port = int(
        os.environ.get("PORT", 5000)
    )
    app.run(
        host="0.0.0.0",
        port=port,
        debug=True
    )
