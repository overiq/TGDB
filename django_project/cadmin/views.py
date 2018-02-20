from django.shortcuts import render, redirect, get_object_or_404, reverse
from blog.forms import PostForm
from django.contrib import messages
from blog.models import Post, Author, Category, Tag
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm

# Create your views here.


def post_add(request):

    # If request is POST, create a bound form (form with data)
    if request.method == "POST":
        f = PostForm(request.POST)

        # check whether form is valid or not
        # if the form is valid, save the data to the database
        # and redirect the user back to the add post form

        # If form is invalid show form with errors again
        if f.is_valid():
            #  save data
            f.save()
            messages.add_message(request, messages.INFO, 'Post added.')
            return redirect('post_add')

    # if request is GET the show unbound form to the user
    else:
        f = PostForm()
    return render(request, 'cadmin/post_add.html', {'form': f})


def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # If request is POST, create a bound form(form with data)
    if request.method == "POST":
        f = PostForm(request.POST, instance=post)

        # check whether form is valid or not
        # if the form is valid, save the data to the database
        # and redirect the user back to the update post form

        # If form is invalid show form with errors again
        if f.is_valid():
            f.save()
            messages.add_message(request, messages.INFO, 'Post updated.')
            return redirect(reverse('post_update', args=[post.id]))

    # if request is GET the show unbound form to the user, along with data
    else:
        f = PostForm(instance=post)

    return render(request, 'cadmin/post_update.html', {'form': f, 'post': post})


@login_required
def home(request):
    return render(request, 'cadmin/admin_page.html')


def login(request, **kwargs):
    if request.user.is_authenticated():
        return redirect('/cadmin/')
    else:
        return auth_views.login(request, **kwargs)


def register(request):
    if request.method == 'POST':
        f = CustomUserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request, 'Account created successfully')
            return redirect('register')

    else:
        f = CustomUserCreationForm()

    return render(request, 'cadmin/register.html', {'form': f})
