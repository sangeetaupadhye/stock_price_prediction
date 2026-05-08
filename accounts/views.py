from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import os
from django.conf import settings
from .utils.data_cleaner import auto_clean_uploaded_file


def register_view(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']

        # Check if email already registered
        if User.objects.filter(username=email).exists():
            return render(request, 'accounts/register.html', {
                'error': 'This email is already registered. Please login.'
            })

        User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=name
        )

        return redirect('login')

    return render(request, 'accounts/register.html')


def login_view(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, username=email, password=password)

        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            #  Show error if login fails
            return render(request, 'accounts/login.html', {
                'error': 'Invalid email or password. Please try again.'
            })

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def upload_file(request):
    data = None
    columns = None
    download_url = None
    stats = None
    error = None

    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']

        if not uploaded_file.name.endswith('.csv'):
            error = "Only CSV files are allowed"
            return render(request, 'accounts/upload.html', {'error': error})

        upload_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)
        with open(upload_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        cleaned_filename = f"cleaned_{uploaded_file.name}"
        cleaned_path = os.path.join(settings.MEDIA_ROOT, cleaned_filename)

        cleaned_df, stats = auto_clean_uploaded_file(upload_path, cleaned_path)
        request.session['latest_file'] = cleaned_filename

        columns = cleaned_df.columns
        data = cleaned_df.values.tolist()
        download_url = settings.MEDIA_URL + cleaned_filename

    return render(request, 'accounts/upload.html', {
        'data': data,
        'columns': columns,
        'download_url': download_url,
        'stats': stats,
        'error': error
    })


def dashboard(request):
    return render(request, 'accounts/dashboard.html')