from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from movies.forms import MovieAddForm, CommentForm
from movies.models import Movie, MovieCrew, MovieRate


def movies_list(request):
    movies = Movie.objects.all().filter(is_valid=True)

    context = {
        'movies': movies,
    }

    return render(request, 'movies/movies_list.html', context=context)


def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    comments = movie.movie_comments.all().filter(status=20)
    genres = movie.genres
    movie_crew = MovieCrew.objects.filter(movie=movie).select_related('crew', 'role')
    directors = []
    writers = []
    actors = []

    for crew in movie_crew:
        if crew.role.title == 'Director':
            directors.append(crew.crew.full_name())
        elif crew.role.title == 'Writer':
            writers.append(crew.crew.full_name())
        elif crew.role.title == 'Actor':
            actors.append(crew.crew.full_name())

    context = {'movie': movie,
               'Directors': directors,
               'Writers': writers,
               'Actors': actors,
               'Genres': genres,
               'Comments': comments
               }

    return render(request, 'movies/movie_detail.html', context=context)


def movie_add(request, form=None):
    if request.user.is_authenticated and request.user.is_staff:
        user = User
        if request.method == 'GET':
            if not form:
                form = MovieAddForm()

            return render(request, 'movies/movie_add.html', context={'form': form, 'User': user})

        elif request.method == 'POST':
            form = MovieAddForm(request.POST, request.FILES)

            if form.is_valid():
                form.save()

                return redirect('movies_list')

        form = MovieAddForm(request.POST, request.FILES)
        request.method = 'GET'
        # return movie_add(request, form)
        return render(request, 'movies/movie_add.html', context={'form': form})
    elif request.user.is_anonymous:
        return redirect('user_login')


def edit_movie(request, pk):
    if request.user.is_authenticated and request.user.is_staff:
        movie = get_object_or_404(Movie, pk=pk)
        if request.method == 'GET':
            form = MovieAddForm(instance=movie)
            context = {
                'form': form,
                'movie': movie
            }
            return render(request, 'movies/edit_movie_form.html', context=context)
        elif request.method == 'POST':
            form = MovieAddForm(request.POST, request.FILES, instance=movie)
            if form.is_valid():
                form.save()
                context = {
                    'form': form,
                    'movie': movie
                }
                return redirect('movie_detail', pk=pk)
            else:
                form = MovieAddForm(instance=movie)
                context = {
                    'form': form,
                    'movie': movie
                }
                return render(request, 'movies/edit_movie_form.html', context=context)
    elif request.user.is_anonymous:
        return redirect('user_login')


def delete_movie(request, pk):
    if request.user.is_authenticated and request.user.is_staff:
        movie = get_object_or_404(Movie, pk=pk)
        movie.is_valid = False
        movie.save()

        return redirect('movies_list')
    elif request.user.is_anonymous:
        return redirect('user_login')


def movie_comment(request, pk=None, comment_form=None):
    if request.user.is_authenticated:
        if request.method == 'GET':
            if not comment_form:
                comment_form = CommentForm()

            context_get = {
                'pk': pk,
                'form': comment_form
            }

            return render(request, 'movies/comment.html', context=context_get)

        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if request.user.is_authenticated:
                if comment_form.is_valid():
                    comment = comment_form.save(commit=False)
                    comment.user = request.user
                    comment.movie = comment_form.movie = Movie.objects.get(pk=pk)
                    comment.save()
                else:
                    redirect('movie_comment', comment_form)

            else:
                return redirect('movie_comment', comment_form)

        return redirect('movie_detail', pk)
    elif request.user.is_anonymous:
        return redirect('user_login')


def movie_rate(request, pk):
    movie = get_object_or_404(Movie, pk=pk, is_valid=True)

    MovieRate.objects.update_or_create(
        movie=movie,
        user=request.user,
        defaults={'rate': int(request.POST.get('rating'))})

    return redirect('movie_detail', pk)
