from django.contrib import admin
from mov.models import Movie
from mov.models import Fav

# Register your models here.
admin.site.register(Movie)
admin.site.register(Fav)
