from django.shortcuts import render, redirect
from django.views import View
from .models import Customer, OrderPlaced, Product, Cart
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class ProductView(View):

    def get(self, request):

        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')

        return render(request, 'app/home.html', {'topwears': topwears, 'bottomwears': bottomwears, 'mobiles': mobiles})


class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            item_already_in_cart = Cart.objects.filter(
                Q(product=product.id) & Q(user=request.user)).exists()

        return render(request, 'app/productdetail.html', {'product': product, 'item_already_in_cart': item_already_in_cart})


@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()

    # print(product_id)
    return redirect('/cart')


@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        totalAmount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        # print(cart_product)
        # print(cart)
        if cart_product:

            for p in cart_product:
                tempamount = (p.quantity) * (p.product.discounted_price)
                amount += tempamount

            totalAmount = amount + shipping_amount

            return render(request, 'app/addtocart.html', {'carts': cart, 'amount': amount, 'totalamount': totalAmount})
        else:
            return render(request, 'app/emptycart.html')


def plus_minus_remove_cart(request):

    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        cmd = request.GET['key']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))

        if cmd == "plus":
            c.quantity += 1
            c.save()

        elif cmd == "minus":
            c.quantity -= 1
            c.save()
        else:
           # print(c.quantity)
            c.delete()

        amount = 0.0
        shipping_amount = 70.0
        totalAmount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user ==
                        request.user]

        if cart_product:

            for p in cart_product:
                tempamount = (p.quantity) * (p.product.discounted_price)
                amount += tempamount

            totalAmount = amount + shipping_amount if amount else 0

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalAmount': totalAmount
        }

        return JsonResponse(data)


def buy_now(request):
    return render(request, 'app/buynow.html')


# return render(request, 'app/profile.html')

@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)

    return render(request, 'app/address.html', {'add': add, 'active': 'btn-primary'})


@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', {'order_placed': op})


def mobile(request, data=None):
    if data == None:
        mobiles = Product.objects.filter(category='M')

    elif data == 'Vivo' or data == 'samsung':
        data.capitalize()
        mobiles = Product.objects.filter(category='M').filter(brand=data)

    return render(request, 'app/mobile.html', {'mobiles': mobiles})


# def login(request):
 #   return render(request, 'app/login.html')


# def customerregistration(request):
 #   return render(request, 'app/customerregistration.html')

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
       # form.order_fields(
        #    field_order=['email', 'username', 'password1', 'password2'])
        return render(request, 'app/customerregistration.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(
                request, 'Congratulation !! Registered Sucessfully')
            form.save()

        return render(request, 'app/customerregistration.html', {'form': form})


@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    totalAmount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    # print(cart_product)
    # print(cart)
    if cart_product:

        for p in cart_product:
            tempamount = (p.quantity) * (p.product.discounted_price)
            amount += tempamount

        totalAmount = amount + shipping_amount if amount else 0

    return render(request, 'app/checkout.html', {'add': add, 'totalamount': totalAmount, 'cart_items': cart_items})


@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    print(custid)
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)

    for c in cart:
        OrderPlaced(user=user, customer=customer,
                    product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect("orders")


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})

    def post(self, request):
        form = CustomerProfileForm(request.POST)

        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr, name=name, locality=locality,
                           city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(
                request, 'Congratulation!! Profile Updated Successfully')

        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})
