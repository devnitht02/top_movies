# top_movies
This Flask app lets users manage a local movie database, adding, editing, and deleting details. Integrated with The Movie Database (TMDb) API, it retrieves movie info like titles, descriptions, and poster images. The app uses Flask for routing, SQLAlchemy for database management, and Flask-WTF for form handling and validation.

--Technologies Used--

Flask: Web framework for building the app’s backend and handling routing.
SQLAlchemy: ORM for database management, interacting with the SQLite database.
SQLite: Lightweight database used to store movie data locally.
Flask-WTF: Integration of WTForms for form creation and validation.
TMDb API: External API used to fetch movie details like title, description, and poster image.
Bootstrap: For responsive and modern UI design, using the Flask-Bootstrap extension.

--How to Run This Application--

1. Clone the Repository:

2. Install Dependencies:
pip install -r requirements.txt

3. Set Environment Variables: 

On macOS/Linux:
export MOVIE_API_KEY=your_tmdb_api_key
export MOVIE_SECRET_KEY=your_flask_secret_key

On Windows (Command Prompt):
set MOVIE_API_KEY=your_tmdb_api_key
set MOVIE_SECRET_KEY=your_flask_secret_key

4. Run the Application:
flask run

That's it!