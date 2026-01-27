from mov.models import Movie, Comment, Fav
from mov.owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.humanize.templatetags.humanize import naturaltime
from django.db.models import Q

from mov.forms import CreateForm, CommentForm
# Create your views here.

class MovieListView(OwnerListView):
    model = Movie
    template_name = "mov/movie_list.html"

    def get(self, request) :
        movie_list = Movie.objects.all()
        favorites = list()
        if request.user.is_authenticated:
            # rows = [{'id': 2}, {'id': 4} ... ]  (A list of rows)
            rows = request.user.mov_favorite_things.values('id')
            print(rows)
            # favorites = [2, 4, ...] using list comprehension
            favorites = [ row['id'] for row in rows ]
        print(favorites)
        ctx = {'movie_list' : movie_list, 'favorites': favorites}
        return render(request, self.template_name, ctx)


class PostListView(View):
    template_name = "mov/movie_list.html"

    def get(self, request) :
        strval =  request.GET.get("search", False)
        if strval :
            # Simple title-only search
            # objects = Post.objects.filter(title__contains=strval).select_related().distinct().order_by('-updated_at')[:10]

            # Multi-field search
            # __icontains for case-insensitive search
            query = Q(title__icontains=strval)
            query.add(Q(text__icontains=strval), Q.OR)
            movie_list = Movie.objects.filter(query).select_related().distinct().order_by('-updated_at')[:10]
        else :
            movie_list = Movie.objects.none()
            # ad_list = Ad.objects.all().order_by('-updated_at')[:10]

        # Augment the ad_list
        for obj in movie_list:
            obj.natural_updated = naturaltime(obj.updated_at)

        favorites = []
        if request.user.is_authenticated:
            rows = request.user.mov_favorite_things.values('id')
            favorites = [row['id'] for row in rows]

        ctx = {
            'movie_list': movie_list,
            'search': strval,
            'favorites': favorites
        }

        return render(request, self.template_name, ctx)



class MovieDetailView(OwnerDetailView):
    model = Movie
    template_name = "mov/movie_detail.html"
    def get(self, request, pk) :
        x = get_object_or_404(Movie, id=pk)
        comments = Comment.objects.filter(movie=x).order_by('-updated_at')
        comment_form = CommentForm()
        context = { 'movie' : x, 'comments': comments, 'comment_form': comment_form }
        return render(request, self.template_name, context)

# class AdCreateView(OwnerCreateView):
#     model = Ad
#     # List Ad model fields to copy to the Ad form / template
#     fields = ['title', 'text', 'price']

class MovieCreateView(LoginRequiredMixin, View):
    template_name = 'mov/movie_form.html'
    success_url = reverse_lazy('mov:all')

    def get(self, request, pk=None):
        form = CreateForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        form = CreateForm(request.POST, request.FILES or None)

        print("POST data:", request.POST)
        print("FILES:", request.FILES)

        if not form.is_valid():

            print("FORM ERRORS:", form.errors)   # 🔴 CRITICAL

            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        # Add owner to the model before saving
        movie = form.save(commit=False)
        movie.owner = self.request.user
        movie.save()

        # https://django-taggit.readthedocs.io/en/latest/forms.html#commit-false
        form.save_m2m()

        return redirect(self.success_url)

# class AdUpdateView(OwnerUpdateView):
#     model = Ad
#     fields = ['title', 'text', 'price']

class MovieUpdateView(LoginRequiredMixin, View):
    template_name = 'mov/movie_form.html'
    success_url = reverse_lazy('mov:all')

    def get(self, request, pk):
        movie = get_object_or_404(Movie, id=pk, owner=self.request.user)
        form = CreateForm(instance=movie)
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        movie = get_object_or_404(Movie, id=pk, owner=self.request.user)
        form = CreateForm(request.POST, request.FILES or None, instance=movie)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        movie = form.save(commit=False)
        movie.save()

        return redirect(self.success_url)


class MovieDeleteView(OwnerDeleteView):
    model = Movie


class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        a = get_object_or_404(Movie, id=pk)
        comment = Comment(text=request.POST['comment'], owner=request.user, movie=a)
        comment.save()
        return redirect(reverse('mov:movie_detail', args=[pk]))

class CommentDeleteView(OwnerDeleteView):
    model = Comment
    template_name = "mov/movie_comment_delete.html"

    # https://stackoverflow.com/questions/26290415/deleteview-with-a-dynamic-success-url-dependent-on-id
    def get_success_url(self):
        movie = self.object.movie
        return reverse('mov:movie_detail', args=[movie.id])

def stream_file(request, pk):
    movie = get_object_or_404(Movie, id=pk)
    response = HttpResponse()
    response['Content-Type'] = movie.content_type
    response['Content-Length'] = len(movie.picture)
    response.write(movie.picture)
    return response



# csrf exemption in class based views
# https://stackoverflow.com/questions/16458166/how-to-disable-djangos-csrf-validation
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError

@method_decorator(csrf_exempt, name='dispatch')
class ToggleFavoriteView(LoginRequiredMixin, View):

    def post(self, request, pk) :
        t = get_object_or_404(Movie, id=pk)
        fav = Fav(user=request.user, movie=t)
        try:
            fav.save()
            return HttpResponse("Favorite added 42")
        except IntegrityError:  # Already there, lets delete...
            Fav.objects.get(user=request.user, thing=t).delete()
            return HttpResponse("Favorite deleted 42")
        return HttpResponse("Something went wrong")


