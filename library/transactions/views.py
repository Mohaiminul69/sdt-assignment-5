from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.http import HttpResponse
from django.views.generic import CreateView, ListView
from transactions.constants import DEPOSIT, BORROW_BOOK, RETURN_BOOK
from datetime import datetime
from django.db.models import Sum
from transactions.forms import (
    DepositForm,
)
from transactions.models import Transaction
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


# Create your views here.
def send_transaction_email(user, amount, mail_subject, template_name):
    message = render_to_string(template_name, {"user": user, "amount": amount})

    send_email = EmailMultiAlternatives(mail_subject, "", to=[user.email])
    send_email.attach_alternative(message, "text/html")
    send_email.send()


class TransactionCreateMixin(LoginRequiredMixin, CreateView):
    template_name = "transaction_form.html"
    model = Transaction
    title = ""
    success_url = reverse_lazy("profile")  # Need to change later

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"account": self.request.user.account})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"title": self.title})

        return context


class DepositMoneyView(TransactionCreateMixin):
    form_class = DepositForm
    title = "Deposit"

    def get_initial(self):
        initial = {"transaction_type": DEPOSIT}
        return initial

    def form_valid(self, form):
        amount = form.cleaned_data.get("amount")
        account = self.request.user.account
        account.balance += amount
        account.save(update_fields=["balance"])

        messages.success(
            self.request,
            f'{"{:,.2f}".format(float(amount))}$ was deposited to your account successfully',
        )

        send_transaction_email(
            self.request.user,
            amount,
            "Deposite Information",
            "deposit_email.html",
        )
        return super().form_valid(form)
