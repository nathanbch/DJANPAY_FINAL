from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()

    return render(request, 'auth/login.html', {'form': form})


@login_required
def home_view(request):
    username = request.user.username
    is_admin = request.user.is_staff

    return render(request, "home.html", {
        "username": username,
        "is_admin": is_admin,
        "user_role": "Administrateur" if is_admin else "Utilisateur"
    })


@login_required
def dashboard_view(request):
    username = request.user.username
    is_admin = request.user.is_staff

    return render(request, "dashboard.html", {
        "username": username,
        "is_admin": is_admin,
        "user_role": "Administrateur" if is_admin else "Utilisateur"
    })


def logout_view(request):
    logout(request)
    return redirect('login')
