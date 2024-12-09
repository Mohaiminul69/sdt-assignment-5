from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from .forms import UserRegistrationForm
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth import login, logout


# Create your views here.
def send_transaction_email(user, account_no, mail_subject, template_name):
    message = render_to_string(template_name, {"user": user, "account_no": account_no})

    send_email = EmailMultiAlternatives(mail_subject, "", to=[user.email])
    send_email.attach_alternative(message, "text/html")
    send_email.send()


class UserRegistrationView(FormView):
    template_name = "registration.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("profile")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "You have been registered to the library")
        return super().form_valid(form)


class UserLoginView(LoginView):
    template_name = "login.html"

    def get_success_url(self):
        messages.success(self.request, "Login Successful")

        return reverse_lazy("homepage")


class UserLogoutView(LogoutView):
    def get_success_url(self):
        if self.request.user.is_authenticated:
            logout(self.request)
        messages.success(self.request, "Logout Successful")
        return reverse_lazy("homepage")


def profile(request):
    return render(request, "profile.html")
