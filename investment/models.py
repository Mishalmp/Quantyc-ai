# investment/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save,pre_delete
from django.dispatch import receiver



class Customer(AbstractUser):
    pass

    def __str__(self):
        return self.username

class Product(models.Model):
    name = models.CharField(max_length=100)
    


class UserProductInvestment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    total_investment_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.customer.username} - {self.product.name} - {self.total_investment_amount}"
    
    class Meta:
        unique_together = ['customer',"product"]


class Transactions(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    investment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    withdraw_money = models.BooleanField(default=False)

    
    def __str__(self):
        return f"{self.customer.username} - {self.product.name} - {self.investment_amount}"
    

@receiver(post_save, sender=Transactions)
def adjust_investment_amount(sender, instance, created, **kwargs):
    user_product_investment, created = UserProductInvestment.objects.get_or_create(
        customer=instance.customer,
        product=instance.product
    )
    if instance.withdraw_money:
        user_product_investment.total_investment_amount -= instance.investment_amount
    else:
        user_product_investment.total_investment_amount += instance.investment_amount
    user_product_investment.save()



@receiver(pre_delete, sender=Transactions)
def revert_adjustment(sender, instance, **kwargs):
    if not instance.withdraw_money:
        user_product_investment = UserProductInvestment.objects.get(
            customer=instance.customer,
            product=instance.product
        )
        user_product_investment.total_investment_amount -= instance.investment_amount
        user_product_investment.save()