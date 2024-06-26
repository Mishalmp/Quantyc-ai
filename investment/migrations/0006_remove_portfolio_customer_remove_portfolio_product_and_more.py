# Generated by Django 5.0.6 on 2024-05-24 12:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investment', '0005_alter_portfolio_product_investment_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='portfolio',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='portfolio',
            name='product',
        ),
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('investment_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('withdraw_money', models.BooleanField(default=False)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='investment.product')),
            ],
        ),
        migrations.DeleteModel(
            name='Investment',
        ),
        migrations.DeleteModel(
            name='Portfolio',
        ),
    ]
