# Generated by Django 5.0.6 on 2024-05-24 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investment', '0003_portfolio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portfolio',
            name='product_investment_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
