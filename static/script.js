const form =
    document.getElementById("movie-form");

const titleInput =
    document.getElementById("title");

const yearInput =
    document.getElementById("year");

const genreInput =
    document.getElementById("genre");

const movieIdInput =
    document.getElementById("movie-id");

const moviesContainer =
    document.getElementById("movies-container");

const movieCount =
    document.getElementById("movie-count");

const searchInput =
    document.getElementById("search");

const formTitle =
    document.getElementById("form-title");

const submitButton =
    document.getElementById("submit-button");

const cancelButton =
    document.getElementById("cancel-button");


let movies = [];
async function loadMovies() {

    const response =
        await fetch("/movies");

    movies =
        await response.json();

    displayMovies(movies);
}
function displayMovies(list) {

    movieCount.textContent =
        `${list.length} movie${list.length !== 1 ? "s" : ""}`;


    if (list.length === 0) {

        moviesContainer.innerHTML = `
            <p class="empty">
                No movies found.
            </p>
        `;

        return;
    }

    moviesContainer.innerHTML =
        list.map(movie => `

            <div class="movie-card">

                <h3>
                    ${escapeHtml(movie.title)}
                </h3>

                <p class="movie-info">
                    📅 ${movie.year}
                </p>

                <span class="genre">
                    ${escapeHtml(movie.genre)}
                </span>

                <div class="card-buttons">

                    <button
                        class="edit-btn"
                        onclick="editMovie(${movie.id})"
                    >
                        Edit
                    </button>

                    <button
                        class="delete-btn"
                        onclick="deleteMovie(${movie.id})"
                    >
                        Delete
                    </button>

                </div>

            </div>

        `).join("");
}

form.addEventListener(
    "submit",
    async function(event) {

        event.preventDefault();


        const id =
            movieIdInput.value;


        const movie = {

            title:
                titleInput.value.trim(),

            year:
                Number(yearInput.value),

            genre:
                genreInput.value

        };


        let response;


        if (id) {

            response =
                await fetch(
                    `/movies/${id}`,
                    {
                        method: "PUT",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify(movie)
                    }
                );

        } else {

            response =
                await fetch(
                    "/movies",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify(movie)
                    }
                );
        }


        const result =
            await response.json();


        if (!response.ok) {

            alert(
                result.error ||
                "Something went wrong."
            );

            return;
        }


        alert(
            id
                ? "Movie updated!"
                : "Movie added!"
        );


        resetForm();

        loadMovies();

    }
);

function editMovie(id) {

    const movie =
        movies.find(
            movie => movie.id === id
        );


    if (!movie) return;


    movieIdInput.value =
        movie.id;

    titleInput.value =
        movie.title;

    yearInput.value =
        movie.year;

    genreInput.value =
        movie.genre;


    formTitle.textContent =
        "Edit Movie";

    submitButton.textContent =
        "Update Movie";

    cancelButton.style.display =
        "block";


    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
}

async function deleteMovie(id) {

    const movie =
        movies.find(
            movie => movie.id === id
        );


    if (!movie) return;


    if (
        !confirm(
            `Delete "${movie.title}"?`
        )
    ) {
        return;
    }


    const response =
        await fetch(
            `/movies/${id}`,
            {
                method: "DELETE"
            }
        );


    const result =
        await response.json();


    if (!response.ok) {

        alert(result.error);

        return;
    }


    alert(
        "Movie deleted successfully!"
    );


    loadMovies();
}

function cancelEdit() {
    resetForm();
}

function resetForm() {

    form.reset();

    movieIdInput.value = "";

    formTitle.textContent =
        "Add a Movie";

    submitButton.textContent =
        "Add Movie";

    cancelButton.style.display =
        "none";
}

searchInput.addEventListener(
    "input",
    function() {

        const search =
            searchInput.value.toLowerCase();


        const filtered =
            movies.filter(movie =>

                movie.title
                    .toLowerCase()
                    .includes(search)

                ||

                movie.genre
                    .toLowerCase()
                    .includes(search)

                ||

                movie.year
                    .toString()
                    .includes(search)
            );


        displayMovies(filtered);
    }
);
function escapeHtml(text) {

    const div =
        document.createElement("div");

    div.textContent =
        text;

    return div.innerHTML;
}

loadMovies();
