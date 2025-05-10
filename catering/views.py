from django.shortcuts import render, redirect
from .models import Client, Event, Menu, Order
from .models import Client
from .models import ContactMessage  # Assuming you store messages in DB
from django.core.mail import send_mail
from django.contrib import messages

def contact(request):
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        subject = request.POST["subject"]
        message = request.POST["message"]

        # Save to database
        ContactMessage.objects.create(name=name, email=email, subject=subject, message=message)

        # Send email (Optional)
        send_mail(
            subject=f"New Contact Message: {subject}",
            message=f"From: {name} ({email})\n\n{message}",
            from_email="your_email@example.com",
            recipient_list=["admin@example.com"],
            fail_silently=True,
        )

        messages.success(request, "Your message has been sent successfully!")
        return redirect("contact")

    return render(request, "contact.html")

def client_list(request):
    clients = Client.objects.all()
    return render(request, "client_list.html", {"clients": clients})

def add_client(request):
    if request.method == "POST":
        name = request.POST.get("name")
        contact = request.POST.get("contact")
        email = request.POST.get("email")
        if name and contact and email:
            Client.objects.create(name=name, contact=contact, email=email)
            return redirect("client_list")  # No extra space!
    return render(request, "add_client.html")

def add_event(request):
    return render(request, 'add_event.html')



def home(request):
    clients = Client.objects.all()  # Fetch all clients
    events = Event.objects.all()  # Fetch all events
    return render(request, 'catering/home.html', {'clients': clients, 'events': events})

from django.shortcuts import render, redirect, get_object_or_404
from .models import Staff
from .forms import StaffForm

def staff_list(request):
    staffs = Staff.objects.all()
    return render(request, 'staff_list.html', {'staffs': staffs})

def add_staff(request):
    if request.method == 'POST':
        form = StaffForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('staff_list')
    else:
        form = StaffForm()
    return render(request, 'add_staff.html', {'form': form})

def delete_staff(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)
    staff.delete()
    return redirect('staff_list')

def edit_staff(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)
    if request.method == 'POST':
        form = StaffForm(request.POST, instance=staff)
        if form.is_valid():
            form.save()
            return redirect('staff_list')
    else:
        form = StaffForm(instance=staff)
    return render(request, 'edit_staff.html', {'form': form, 'staff': staff})

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from .forms import RegisterForm, LoginForm, ForgotPasswordForm, ResetPasswordForm

def register_view(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        return redirect('login')
    return render(request, 'catering/register.html', {'form': form})

def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if user:
            login(request, user)
            return redirect('home')  # Replace with your home URL name
    return render(request, 'catering/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def forgot_password_view(request):
    form = ForgotPasswordForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save(
            request=request,
            use_https=request.is_secure(),
            email_template_name='catering/password_reset_email.html',
        )
        return redirect('login')
    return render(request, 'catering/forgot_password.html', {'form': form})

def reset_password_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception:
        user = None

    if user and default_token_generator.check_token(user, token):
        form = ResetPasswordForm(user, request.POST or None)
        if request.method == 'POST' and form.is_valid():
            form.save()
            return redirect('login')
        return render(request, 'catering/reset_password.html', {'form': form})
    return redirect('forgot_password')
