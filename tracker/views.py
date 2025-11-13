from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import IntegrityError
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
import re
from .models import TrackingHistory, CurrentBalance, UserProfile
from django.http import JsonResponse

# Use the active User model
User = get_user_model()


def check_availability(request):
    field = request.GET.get('field')
    value = request.GET.get('value')
    response = {'exists': False, 'message': ''}

    if field == 'username':
        if User.objects.filter(username=value).exists():
            response = {'exists': True, 'message': 'Username already exists'}
    elif field == 'email':
        if User.objects.filter(email=value).exists():
            response = {'exists': True, 'message': 'Email already exists'}
    elif field == 'phone_number':
        if User.objects.filter(phone_number=value).exists():
            response = {'exists': True, 'message': 'Phone number already exists'}

    return JsonResponse(response)



def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('/')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('/login/')

    return render(request, 'login.html')


def register_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        profile_picture = request.FILES.get('profile_picture')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        # ✅ Validate phone number
        if not re.match(r'^[0-9]{10}$', phone_number):
            messages.error(request, "Phone number must be exactly 10 digits.")
            return redirect('/register/')

        # ✅ Validate username (lowercase letters only)
        if not re.match(r'^[a-z]+$', username):
            messages.error(request, "Username must contain only lowercase letters without spaces.")
            return redirect('/register/')

        # ✅ Check for existing username
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Try New")
            return redirect('/register/')

        # ✅ Check for existing email
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists. Try New")
            return redirect('/register/')

        # ✅ Check for existing phone number
        if User.objects.filter(phone_number=phone_number).exists():
            messages.error(request, "Phone number already exists. Try New")
            return redirect('/register/')

        try:
            # ✅ Create user safely
            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password,
                phone_number=phone_number
            )

            # ✅ Create user profile
            UserProfile.objects.create(
                user=user,
                phone_number=phone_number,
                profile_picture=profile_picture if profile_picture else 'default.jpg'
            )

            messages.success(request, "Account created successfully! You can login now.")
            return redirect('/login/')

        except IntegrityError:
            messages.error(request, "An unexpected error occurred. Please try again.")
            return redirect('/register/')

    return render(request, 'register.html')


def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect('/login/')


@login_required(login_url="login_view")
def base(request):
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        description = request.POST.get('description')
        amount = float(request.POST.get('amount'))
        expense_type = request.POST.get('expense_type')

        current_balance, _ = CurrentBalance.objects.get_or_create(user=request.user)

        if amount <= 0:
            messages.warning(request, "Please enter a valid amount greater than 0.")
            return redirect('/')

        if not expense_type:
            messages.warning(request, "Please select Income or Expense.")
            return redirect('/')

        TrackingHistory.objects.create(
            user=request.user,
            current_balance=current_balance,
            amount=amount,
            expense_type=expense_type,
            description=description
        )

        if expense_type == "INCOME":
            current_balance.current_balance += amount
        else:
            current_balance.current_balance -= amount

        current_balance.save()
        messages.success(request, f"{expense_type.title()} added successfully!")
        return redirect('/')

    current_balance, _ = CurrentBalance.objects.get_or_create(user=request.user)
    transactions = TrackingHistory.objects.filter(user=request.user)
    income = sum(t.amount for t in transactions if t.expense_type == "INCOME")
    expense = sum(t.amount for t in transactions if t.expense_type == "EXPENSE")

    context = {
        'income': income,
        'expense': expense,
        'transactions': transactions,
        'current_balance': current_balance,
        'profile': user_profile,
    }
    return render(request, 'base.html', context)


@login_required(login_url="login_view")
def delete_transaction(request, id):
    tracking_history = TrackingHistory.objects.filter(id=id, user=request.user).first()

    if tracking_history:
        current_balance, _ = CurrentBalance.objects.get_or_create(user=request.user)

        # ✅ Adjust balance correctly based on transaction type
        if tracking_history.expense_type == "INCOME":
            current_balance.current_balance -= tracking_history.amount
        elif tracking_history.expense_type == "EXPENSE":
            current_balance.current_balance += tracking_history.amount

        current_balance.save()
        tracking_history.delete()

    return redirect('/')




@login_required(login_url="login_view")
def edit_transaction(request, tx_id):
    # ✅ Make sure this transaction belongs to the logged-in user
    tx = get_object_or_404(TrackingHistory, id=tx_id, user=request.user)
    current_balance, _ = CurrentBalance.objects.get_or_create(user=request.user)

    if request.method == "POST":
        description = request.POST.get('description', '').strip()
        try:
            amount = float(request.POST.get('amount'))
        except (TypeError, ValueError):
            messages.error(request, "Enter a valid amount.")
            return redirect(request.path)

        expense_type = request.POST.get('expense_type')

        if amount <= 0:
            messages.error(request, "Amount must be greater than zero.")
            return redirect(request.path)

        if expense_type not in ("INCOME", "EXPENSE"):
            messages.error(request, "Please select a valid type.")
            return redirect(request.path)

        # 🧮 Undo previous transaction impact
        if tx.expense_type == "INCOME":
            current_balance.current_balance -= tx.amount
        else:  # was EXPENSE
            current_balance.current_balance += tx.amount

        # 🧮 Apply new transaction impact
        if expense_type == "INCOME":
            current_balance.current_balance += amount
        else:
            current_balance.current_balance -= amount

        # 💾 Save changes
        tx.description = description
        tx.amount = amount
        tx.expense_type = expense_type
        tx.save()
        current_balance.save()

        messages.success(request, "Transaction updated successfully!")
        return redirect('/')

    # GET request → show form with pre-filled data
    context = {'tx': tx}
    return render(request, 'edit_transaction.html', context)




@login_required
def edit_profile(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        profile_picture = request.FILES.get('profile_picture')

        if not re.match(r'^[0-9]{10}$', phone_number):
            messages.error(request, "Phone number must be 10 digits.")
            return redirect('edit_profile')

        profile.phone_number = phone_number
        request.user.email = email
        request.user.save()

        if profile_picture:
            profile.profile_picture = profile_picture

        profile.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('/')

    context = {'profile': profile}
    return render(request, 'edit_profile.html', context)



def health_check(request):
    return JsonResponse({"status": "ok"}, status=200)
