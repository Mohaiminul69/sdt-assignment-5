# Generated by Django 5.1.2 on 2024-12-10 16:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Transaction",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("amount", models.DecimalField(decimal_places=2, max_digits=12)),
                (
                    "balance_after_transaction",
                    models.DecimalField(decimal_places=2, max_digits=12),
                ),
                (
                    "transaction_type",
                    models.IntegerField(
                        choices=[
                            (1, "Deposite"),
                            (2, "Borrow Book"),
                            (3, "Return Book"),
                        ],
                        null=True,
                    ),
                ),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="transactions",
                        to="accounts.useraccount",
                    ),
                ),
            ],
            options={
                "ordering": ["timestamp"],
            },
        ),
    ]