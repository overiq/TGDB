from django.shortcuts import render, redirect, get_object_or_404, reverse, Http404
from blog.forms import PostForm, CategoryForm, TagForm
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
    # If request is POST, create a bound form(form with data)
    if request.method == "POST":
        f = PostForm(request.POST)

        # check whether form is valid or not
        # if the form is valid, save the data to the database
        # and redirect the user back to the add post form

        # If form is invalid show form with errors again
        if f.is_valid():
            # if author is not selected and user is superuser, then assign the post to the author named staff
            if request.POST.get('author') == "" and request.user.is_superuser:
                new_post = f.save(commit=False)
                author = Author.objects.get(user__username='staff')
                new_post.author = author
                new_post.save()
                f.save_m2m()

            # if author is selected and user is superuser
            elif request.POST.get('author') and request.user.is_superuser:
                new_post = f.save()

            # if user is not a superuser
            else:
                new_post = f.save(commit=False)
                new_post.author = Author.objects.get(user__username=request.user.username)
                new_post.save()
                f.save_m2m()

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
            # if author is not selected and user is superuser, then assign the post to the author named staff
            if request.POST.get('author') == "" and request.user.is_superuser:
                updated_post = f.save(commit=False)
                author = Author.objects.get(user__username='staff')
                updated_post.author = author
                updated_post.save()
                f.save_m2m()
            # if author is selected and user is superuser
            elif request.POST.get('author') and request.user.is_superuser:
                updated_post = f.save()
            # if user is not a superuser
            else:
                updated_post = f.save(commit=False)
                updated_post.author = Author.objects.get(user__username=request.user.username)
                updated_post.save()
                f.save_m2m()

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
                    is_active=0,
                    is_staff=True
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


@login_required
def post_list(request):
    if request.user.is_superuser:
        posts = Post.objects.order_by("-id").all()
    else:
        posts = Post.objects.filter(author__user__username=request.user.username).order_by("-id")

    posts = helpers.pg_records(request, posts, 5)

    return render(request, 'cadmin/post_list.html', {'posts': posts})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    next_page = request.GET['next']
    messages.add_message(request, messages.INFO, 'Post deleted')
    return redirect(next_page)


@login_required
def category_list(request):
    if request.user.is_superuser:
        categories = Category.objects.order_by("-id").all()
    else:
        categories = Category.objects.filter(author__user__username=request.user.username).order_by("-id")

    categories = helpers.pg_records(request, categories, 5)

    return render(request, 'cadmin/category_list.html', {'categories': categories})


# view to add new category
@login_required
def category_add(request):

    # If request is POST, create a bound form(form with data)
    if request.method == "POST":
        f = CategoryForm(request.POST)

        # check whether form is valid or not
        # if the form is valid, save the data to the database
        # and redirect the user back to the add post form

        # If form is invalid show form with errors again
        if f.is_valid():
            # new_category = f.save()
            # new_category = f.save(commit=False)
            # new_category.author = get_user(request)
            # new_category.save()

            if request.POST.get('author') == "" and request.user.is_superuser:
                # if author is not supplied and user is superuser
                new_category = f.save(commit=False)
                author = Author.objects.get(user__username='staff')
                new_category.author = author
                new_category.save()
            elif request.POST.get('author') and request.user.is_superuser:
                # if author is supplied and user is superuser
                new_category = f.save()
            else:
                # if author not a superuser
                new_category = f.save(commit=False)
                new_category.author = Author.objects.get(user__username=request.user.username)
                new_category.save()

            messages.add_message(request, messages.INFO, 'Category added')
            return redirect('category_add')

    # if request is GET the show unbound form to the user
    else:
        f = CategoryForm()

    return render(request, 'cadmin/category_add.html', {'form': f})


# view to update category
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)

    # If request is POST, create a bound form(form with data)
    if request.method == "POST": # If request is POST, create a bound form
        f = CategoryForm(request.POST, instance=category)

        # check whether form is valid or not
        # if the form is valid, save the data to the database
        # and redirect the user back to the category form

        # If form is invalid show form with errors again
        if f.is_valid():

            if request.POST.get('author') == "" and request.user.is_superuser:
                # if author is not supplied and user is superuser
                updated_category = f.save(commit=False)
                author = Author.objects.get(user__username='staff')
                updated_category.author = author
                updated_category.save()
            elif request.POST.get('author') and request.user.is_superuser:
                # if author is supplied and user is superuser
                updated_category = f.save()
            else:
                # if author not a superuser
                updated_category = f.save(commit=False)
                updated_category.author = Author.objects.get(user__username=request.user.username)
                updated_category.save()

            new_category = f.save()
            messages.add_message(request, messages.INFO, 'Category updated')
            return redirect(reverse('category_update', args=[category.id]))

    # if request is GET the show unbound form to the user
    else:
        f = CategoryForm(instance=category)

    return render(request, 'cadmin/category_update.html', {'form': f, 'category': category})


@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    next_page = request.GET['next']
    messages.add_message(request, messages.INFO, 'Category deleted')
    return redirect(next_page)


# view to add list all tags
@login_required
def tag_list(request):
    if request.user.is_superuser:
        tags = Tag.objects.order_by("-id").all()
    else:
        tags = Tag.objects.filter(author__user__username=request.user.username).order_by("-id")

    tags = helpers.pg_records(request, tags, 5)
    return render(request, 'cadmin/tag_list.html', {'tags': tags})


# view to add new tag
@login_required
def tag_add(request):

    # If request is POST, create a bound form(form with data)
    if request.method == "POST":
        f = TagForm(request.POST)

        # check whether form is valid or not
        # if the form is valid, save the data to the database
        # and redirect the user back to the add post form

        # If form is invalid show form with errors again
        if f.is_valid():
            # new_category = f.save()
            # new_category = f.save(commit=False)
            # new_category.author = get_user(request)
            # new_category.save()

            if request.POST.get('author') == "" and request.user.is_superuser:
                # if author is not supplied and user is superuser
                new_tag = f.save(commit=False)
                author = Author.objects.get(user__username='staff')
                new_tag.author = author
                new_tag.save()
            elif request.POST.get('author') and request.user.is_superuser:
                # if author is supplied and user is superuser
                new_tag = f.save()
            else:
                # if author not a superuser
                new_tag = f.save(commit=False)
                new_tag.author = Author.objects.get(user__username=request.user.username)
                new_tag.save()

            messages.add_message(request, messages.INFO, 'Tag added')
            return redirect('tag_add')

    # if request is GET the show unbound form to the user
    else:
        f = TagForm()

    return render(request, 'cadmin/tag_add.html', {'form': f})


# view to update tag
@login_required
def tag_update(request, pk):
    tag = get_object_or_404(Tag, pk=pk)

    # If request is POST, create a bound form(form with data)
    if request.method == "POST": # If request is POST, create a bound form
        f = TagForm(request.POST, instance=tag)

        # check whether form is valid or not
        # if the form is valid, save the data to the database
        # and redirect the user back to the tag update form

        # If form is invalid show form with errors again
        if f.is_valid():
            # updated_tag = f.save()

            if request.POST.get('author') == "" and request.user.is_superuser:
                # if author is not supplied and user is superuser
                updated_tag = f.save(commit=False)
                author = Author.objects.get(user__username='staff')
                updated_tag.author = author
                updated_tag.save()
            elif request.POST.get('author') and request.user.is_superuser:
                # if author is supplied and user is superuser
                updated_tag = f.save()
            else:
                # if author not a superuser
                updated_tag = f.save(commit=False)
                updated_tag.author = Author.objects.get(user__username=request.user.username)
                updated_tag.save()

            messages.add_message(request, messages.INFO, 'Tag updated')
            return redirect(reverse('tag_update', args=[tag.id]))

    # if request is GET the show unbound form to the user
    else:
        f = TagForm(instance=tag)

    return render(request, 'cadmin/tag_update.html', {'form': f, 'tag': tag})


@login_required
def tag_delete(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    tag.delete()
    next_page = request.GET['next']
    messages.add_message(request, messages.INFO, 'Tag deleted')
    return redirect(next_page)


@login_required
def account_info(request):
    return render(request, 'cadmin/account_info.html')
