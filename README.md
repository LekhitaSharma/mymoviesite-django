Hello,
Lekhita here.

This is my first django project. 

Movie Review Web App | Django, Python, HTML, API
• Built a full-stack Django application with user authentication and CRUD functionality.
• Implemented form handling using django-crispy-forms and Bootstrap.

What this website can do - this is a personal movie review site. 
    - You can add a movie, add a review, comments, an img file and tags for the said movie.
    - This is all connected to a MYSQL database.
    - You can also search more details for a Movie by clicking on the entry you added, it will take you a detail page where you will have an option to click on a 'get more details' button which will take you to a page with more details like - Release year, IMDB Rating, Director and Cast Info ( with their individual wikipedia page linked ), Awards won and Plot summary. These details for the Movie detail page are being pulled using OMDBAPI.

Features in Detail 
    - User Authentication — Sign up, login, logout, password reset
    - CRUD for Movies — Add, edit, delete your own movies (owner-based permissions)
    - Rich Relationships
    - One-to-Many: User → Movies
    - Many-to-Many: Movies ↔ Tags/Genres
    - Image Uploads — Poster upload with Django media handling
    - Tags & Filtering — Add custom tags, filter by genre/tag
    - APIs — Auto-fetch movie details (title, year, plot, poster) from TMDB API when you enter a movie name
    - Admin Panel — Full Django admin for movies, users, tags
    - Responsive UI — Clean HTML/CSS templates
