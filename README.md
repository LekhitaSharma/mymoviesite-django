🎬 Movie Review Web App
Hello, Lekhita here. This is my first Django project.

Stack: Django • Python • HTML • API • MySQL • Bootstrap

Built a full-stack Django application with user authentication and CRUD functionality. Implemented form handling using django-crispy-forms and Bootstrap.

What this website can do
This is a personal movie review site where you can:

Add a movie, add a review, comments, an image file, and tags
Store everything in a MySQL database
Click any movie entry to open a detail page
Hit 'Get More Details' to auto-pull data from OMDb API:
Release year, IMDb Rating
Director and Cast info (with individual Wikipedia links)
Awards won
Plot summary
Features in Detail
User Authentication

Sign up, login, logout, password reset
CRUD for Movies

Add, edit, delete your own movies (owner-based permissions)
Rich Relationships

One-to-Many: User → Movies
Many-to-Many: Movies ↔ Tags/Genres
Image Uploads

Poster upload with Django media handling
Tags & Filtering

Add custom tags, filter by genre/tag
APIs

Auto-fetch movie details (title, year, plot, poster) from OMDb API
Admin Panel

Full Django admin for movies, users, tags
Responsive UI

Clean HTML/CSS templates with Bootstrap
Tech Used
Django 4.x, Python 3.11
django-crispy-forms + Bootstrap 4
MySQL
Pillow (image uploads)
Requests (OMDb API)
