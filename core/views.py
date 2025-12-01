from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db import transaction as db_transaction
from .forms import TransferForm
from .models import Account, Transaction

User = get_user_model()


def is_admin(user):
    return user.is_staff


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("dashboard")
        messages.error(request, "Identifiants invalides.")
    else:
        form = AuthenticationForm()
    return render(request, "auth/login.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "Vous avez été déconnecté.")
    return redirect("login")


@login_required
def dashboard_view(request):
    if request.user.is_staff:
        return render(request, "dashboard_admin.html", {"user": request.user})
    return render(request, "dashboard_user.html", {"user": request.user})


@login_required
def home_view(request):
    return render(request, "home.html", {
        "username": request.user.username,
        "is_admin": request.user.is_staff,
    })


@login_required
@user_passes_test(is_admin)
def admin_panel(request):
    users = User.objects.all()
    return render(request, "admin_panel.html", {"users": users})


@login_required
@user_passes_test(is_admin)
def create_user_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        is_staff = request.POST.get('is_staff') == 'on'

        User.objects.create_user(
            username=username,
            password=password,
            is_staff=is_staff
        )
        messages.success(request, "Utilisateur créé avec succès.")
        return redirect('admin_panel')

    return render(request, "create_user.html")


@login_required
def transfer_view(request):
    sender = request.user
    sender_account = get_object_or_404(Account, user=sender)

    if request.method == "POST":
        form = TransferForm(request.POST, user=request.user)
        if form.is_valid():
            receiver_username = form.cleaned_data["receiver_username"]
            amount = form.cleaned_data["amount"]
            description = form.cleaned_data["description"]

            receiver = get_object_or_404(User, username=receiver_username)
            receiver_account = get_object_or_404(Account, user=receiver)

            if sender_account.balance < amount:
                messages.error(request, "Solde insuffisant.")
                return redirect("transfer")

            with db_transaction.atomic():
                sender_account.balance -= amount
                receiver_account.balance += amount
                sender_account.save()
                receiver_account.save()

                Transaction.objects.create(
                    sender=sender,
                    receiver=receiver,
                    amount=amount,
                    description=description,
                )

            messages.success(request, "Virement effectué avec succès.")
            return redirect("dashboard")
    else:
        form = TransferForm(user=request.user)

    return render(request, "transfer.html", {
        "form": form,
        "balance": sender_account.balance,
    })


@login_required
def account_view(request):
    account = get_object_or_404(Account, user=request.user)
    return render(request, "account.html", {"account": account})


@login_required
def history_view(request):
    transactions = Transaction.objects.filter(
        sender=request.user
    ).order_by('-timestamp')
    return render(request, "history.html", {"transactions": transactions})


@login_required
def profile_view(request):
    return render(request, "profile.html", {"user": request.user})


@login_required
def delete_account(request):
    if request.method == "POST":
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, "Votre compte a été supprimé.")
        return redirect("login")
    return render(request, "delete_account_confirm.html")
