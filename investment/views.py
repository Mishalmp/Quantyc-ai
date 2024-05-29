
from django.views.generic import View, CreateView
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render, redirect
from .forms import LoginForm, RegistrationForm,InvestmentForm
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import RedirectView
from .models import Product,Transactions,Customer,UserProductInvestment
from django.http import JsonResponse, QueryDict
from decimal import Decimal
#-------------------Account Registration/Authentication--------------------
class LoginView(View):
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.get_redirect_url())
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(self.get_redirect_url())
            else:
                return render(request, self.template_name, {'form': form, 'error': 'Invalid credentials'})
        else:
            return render(request, self.template_name, {'form': form})

    def get_redirect_url(self):
        return reverse_lazy('investment:dashboard')



class RegistrationView(SuccessMessageMixin, CreateView):
    template_name = 'registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('investment:login')
    success_message = "Your account has been created successfully. Please log in."

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
    

from django.conf import settings

class LogoutView(LoginRequiredMixin, RedirectView):
    url = settings.LOGIN_URL  # Redirect URL after logout
    permanent = False  # Redirect is temporary
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        logout(self.request)
        return super().get_redirect_url(*args, **kwargs)



#---------------------Dashboard views---------------------------
class DashboardView(LoginRequiredMixin, View):
    template_name = 'index.html'

    def get(self, request):
        products = Product.objects.all()
        portfolios = UserProductInvestment.objects.filter(customer=request.user)
        form = InvestmentForm()
        context = {
            'products': products,
            'portfolios': portfolios,
            'form': form
        }
        print(context["portfolios"],'------------------------------------')
        return render(request, self.template_name, context)

    def post(self, request):
        form = InvestmentForm(request.POST)
        if form.is_valid():
            investment = form.save(commit=False)
            investment.customer = request.user
            investment.save()

            total_product_user = UserProductInvestment.objects.get(
                customer=request.user,
                product=investment.product
            )

            response_data = {
                'customer': total_product_user.customer.username,
                'product': total_product_user.product.name,
                'investment_amount': str(total_product_user.total_investment_amount),
                'customer_id': total_product_user.customer.id,
                'product_id': total_product_user.product.id
            }
            return JsonResponse(response_data)
        else:
            return JsonResponse({'error': 'Invalid form'}, status=400)
    
    
    def put(self, request):
        data = QueryDict(request.body)
        customer_id = data.get('customer_id')
        product_id = data.get('product_id')
        investment_amount = Decimal(data.get('investment_amount'))
        transaction_type = data.get('transaction_type')

        try:
            user_product_investment = UserProductInvestment.objects.get(
                customer_id=customer_id,
                product_id=product_id
            )

            if transaction_type == 'withdraw':
                if user_product_investment.total_investment_amount - investment_amount < 0:
                    return JsonResponse({'status': 'error', 'message': 'Withdrawal amount cannot be greater than the current investment amount'})
                user_product_investment.total_investment_amount -= investment_amount
            else:
                user_product_investment.total_investment_amount += investment_amount
                


            user_product_investment.save()

            response_data = {
                'customer_id': customer_id,
                'product_id': product_id,
                'investment_amount': str(user_product_investment.total_investment_amount)
            }
            return JsonResponse(response_data)

        except UserProductInvestment.DoesNotExist:
            return JsonResponse({'error': 'Investment not found.'}, status=404)
            
    def delete(self, request, investment_id):
        try:
            # Retrieve the investment object
            investment = UserProductInvestment.objects.get(pk=investment_id)
            investment.delete()
            return JsonResponse({"status": "success", "message": "Investment deleted successfully"})
        except UserProductInvestment.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Investment not found"}, status=404)