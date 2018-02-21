from django.shortcuts import render, redirect, get_object_or_404, reverse, Http404
from blog.forms import PostForm
from django.contrib import messages
from blog.models import Post, Author, Category, Tag
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from django_project import helpers
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.conf import settings

# Create your views here.


@login_required
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


@login_required
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
            # send email verification now
            activation_key = helpers.generate_activation_key(username=request.POST['username'])

            subject = "TheGreatDjangoBlog Account Verification"

            message = '''\n
            Please visit the following link to verify your account \n\n{0}://{1}/cadmin/activate/account/?key={2}
                                    '''.format(request.scheme, request.get_host(), activation_key)

            error = False

            try:
                send_mail(subject, message, settings.SERVER_EMAIL, [request.POST['email']])
                messages.add_message(request, messages.INFO,
                                     'Account created! Click on the link sent to your email to activate the account')

            except:
                error = True
                messages.add_message(request, messages.INFO, 'Unable to send email verification. Please try again')

            if not error:
                u = User.objects.create_user(
                    request.POST['username'],
                    request.POST['email'],
                    request.POST['password1'],
                    is_active=0
                )

                author = Author()
                author.activation_key = activation_key
                author.user = u
                author.save()

            return redirect('register')

    else:
        f = CustomUserCreationForm()

    return render(request, 'cadmin/register.html', {'form': f})


def activate_account(request):
    key = request.GET['key']
    if not key:
        raise Http404()

    r = get_object_or_404(Author, activation_key=key, email_validated=False)
    r.user.is_active = True
    r.user.save()
    r.email_validated = True
    r.save()

    return render(request, 'cadmin/activated.html')