from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm, PostForm, LikeForm, CommentForm
from .models import UserModel, SessionToken, PostModel, LikeModel, CommentModel
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from datetime import timedelta
from django.utils import timezone
from project3.settings import *
from imgurpython import ImgurClient

def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # saving data to DB
            user = UserModel(name=name, password=make_password(password), email=email, username=username)
            user.save()
            return redirect('login/')

    else:
        form = SignUpForm()

    return render(request, 'index.html', {'form': form, 'STATIC_URL': STATIC_URL})


def login_view(request):
    response_data = {}
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user1 = UserModel.objects.filter(username=username).first()

            if user1:
                if check_password(password, user1.password):
                    token = SessionToken(user=user1)
                    token.create_token()
                    token.save()
                    response = redirect("/feed/")
                    response.set_cookie(key='session_token', value=token.session_token)
                    return response
                else:
                    response_data['message'] = 'Incorrect Password! Please try again!'
    elif request.method == 'GET':
        form = LoginForm()

    response_data['form'] = form
    response_data['STATIC_URL'] = STATIC_URL
    return render(request, 'login.html', response_data)


def post_view(request):
    user = check_validation(request)

    if user:
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                image = form.cleaned_data.get('image')
                caption = form.cleaned_data.get('caption')
                post = PostModel(user=user, image=image, caption=caption)
                post.save()

                path = str(post.image.url)

                client = ImgurClient("c62b00a7ad546c3", "9fb1bfb6016f30f0d7123164ad8cb3d3669036f2")
                post.image_url = client.upload_from_path(path, config=None, anon=True)['link']
                post.save()
                return redirect('/feed/')

        else:
            form = PostForm()
        return render(request, 'post.html', {'form': form})
    else:
        return redirect('/login/')


def feed_view(request):
    response_data = {}
    response_data['STATIC_URL'] = STATIC_URL
    user = check_validation(request)
    if user:

        posts = PostModel.objects.all().order_by('created_on')

        for post in posts:
            existing_like = LikeModel.objects.filter(post_id=post.id, user=user).first()
            if existing_like:
                post.has_liked = True

        return render(request, 'feed.html', response_data)
    else:
        return redirect('/login/')



def like_view(request):
    user = check_validation(request)
    if user and request.method == 'POST':
        form = LikeForm(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get('post').id
            existing_like = LikeModel.objects.filter(post_id=post_id, user=user).first()
            if not existing_like:
                LikeModel.objects.create(post_id=post_id, user=user)
            else:
                existing_like.delete()
            return redirect('/feed/')
    else:
        return redirect('/login/')


def comment_view(request):
    user = check_validation(request)
    if user and request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get('post').id
            comment_text = form.cleaned_data.get('comment_text')
            comment = CommentModel.objects.create(user=user, post_id=post_id, comment_text=comment_text)
            comment.save()
            return redirect('/feed/')
        else:
            return redirect('/feed/')
    else:
        return redirect('/login')


# For validating the session
def check_validation(request):
    if request.COOKIES.get('session_token'):
        session = SessionToken.objects.filter(session_token=request.COOKIES.get('session_token')).first()
        if session:
            time_to_live = session.created_on + timedelta(days=1)
            if time_to_live > timezone.now():
                return session.user
    else:
        return None


def log_out(request):
    if request.COOKIES.get('session_token'):
        response = redirect("/feed")
        response.set_cookie(key='session_token', value=None)
        return response
    else:
        return None

def first_view(request):
    response_data = {}
    response_data['STATIC_URL'] = STATIC_URL
    return render(request, 'first.html', response_data)

def sec_view(request):
    response_data = {}
    response_data['STATIC_URL'] = STATIC_URL
    return render(request, 'login.html', response_data)

def third_view(request):
    response_data = {}
    response_data['STATIC_URL'] = STATIC_URL
    return render(request, 'signup.html', response_data)


def rest_view(request):
    response_data = {}
    response_data['STATIC_URL'] = STATIC_URL
    return render(request, 'rest.html', response_data)
def food_view(request):
    response_data = {}
    response_data['STATIC_URL'] = STATIC_URL
    return render(request, 'food.html', response_data)

