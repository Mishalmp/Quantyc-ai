from django.contrib import admin
from .models import Customer,Product,Transactions,UserProductInvestment
# Register your models here.
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Transactions)
admin.site.register(UserProductInvestment)
