# Generated by Django 5.0.6 on 2024-05-24 13:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investment', '0006_remove_portfolio_customer_remove_portfolio_product_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProductInvestment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_investment_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='investment.product')),
            ],
        ),
    ]