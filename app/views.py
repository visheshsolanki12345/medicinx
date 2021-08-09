from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced
from .forms import CustomerPrfileForm, CustomerRegistrationForm, CustomerRegistrationForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Product
from django.views.decorators.csrf import csrf_exempt
from .PayTm import Checksum
# from django.core.mail import send_mail
from django.core.mail import EmailMessage
MERCHANT_KEY = '@fzp_H%SrTa09MJV'



class ProductView(View):
    def get(self,request):
        total_item = 0
        if request.user.is_authenticated:
            total_item = len(Cart.objects.filter(user=request.user))
        syrups = Product.objects.filter(category='S')
        medicines = Product.objects.filter(category='M')
        proteins = Product.objects.filter(category='P')
        tubes = Product.objects.filter(category='T')
        return render(request, 'app/home.html', {'syrups':syrups, 'medicines':medicines, 'proteins':proteins, 'tubes':tubes, 'total_item':total_item})



class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        total_item = 0
        item_already_in_cart = False
        if request.user.is_authenticated:
            total_item = len(Cart.objects.filter(user=request.user))
        if request.user.is_authenticated:
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        return render(request, 'app/productdetail.html', {'product':product, 'item_already_in_cart':item_already_in_cart, 'total_item':total_item})


@login_required
def add_to_cart(request):
    user = request.user
    product_id  = request.GET.get('prod_id') 
    product = Product.objects.get(id=product_id)
    qs = Cart.objects.filter(product=product)
    exists = qs.exists()
    if exists:
        return redirect('/cart')
    Cart(user=user, product=product).save()
    return redirect('/cart')


@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        total_item = 0
        if request.user.is_authenticated:
            total_item = len(Cart.objects.filter(user=request.user))
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                totalamount = amount + shipping_amount
            return render(request, 'app/addtocart.html', {'carts':cart, 'totalamount':totalamount, 'amount':amount, 'total_item':total_item})
        else:
            return render(request, 'app/emptycart.html')


def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]

        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            

        data = {
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':amount + shipping_amount
            }
        return JsonResponse(data)
            

def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]

        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount

        data = {
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':amount + shipping_amount
            }
        return JsonResponse(data)
            

def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]

        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount

        data = {
            'amount':amount,
            'totalamount':amount + shipping_amount
            }
        return JsonResponse(data)
            


@login_required
def profile(request):
    total_item = 0
    if request.user.is_authenticated:
        total_item = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/profile.html', {'total_item':total_item})

@login_required
def address(request):
    total_item = 0
    if request.user.is_authenticated:
        total_item = len(Cart.objects.filter(user=request.user))
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'add':add, 'active':'btn-primary', 'total_item':total_item})


@login_required
def orders(request):
    total_item = 0
    if request.user.is_authenticated:
        total_item = len(Cart.objects.filter(user=request.user))
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', {'order_placed':op, 'total_item':total_item})


@login_required
def protein(request, data=None):
    total_item = 0
    if request.user.is_authenticated:
        total_item = len(Cart.objects.filter(user=request.user))
        proteins = Product.objects.filter(category='P')
    return render(request, 'app/protein.html', {'proteins':proteins, 'total_item':total_item})


@login_required
def tube(request, data=None):
    total_item = 0
    if request.user.is_authenticated:
        total_item = len(Cart.objects.filter(user=request.user))
    tubes = Product.objects.filter(category='T')
    return render(request, 'app/tube.html', {'tubes':tubes, 'total_item':total_item})


@login_required
def syrup(request, data=None):
    total_item = 0
    if request.user.is_authenticated:
        total_item = len(Cart.objects.filter(user=request.user))
        syrups = Product.objects.filter(category='S')
    return render(request, 'app/syrup.html', {'syrups':syrups, 'total_item':total_item})


@login_required
def medicine(request, data=None):
    total_item = 0
    if request.user.is_authenticated:
        total_item = len(Cart.objects.filter(user=request.user))
        medicines = Product.objects.filter(category='M')
    return render(request, 'app/medicine.html', {'medicines':medicines, 'total_item':total_item})



def login(request):
 return render(request, 'app/login.html')




class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form':form})
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations!! Registered Successfully')
            form.save()
            return redirect('login')
        return render(request, 'app/customerregistration.html', {'form':form})
        


##=============================== buy now ========================================## 
@login_required
def buy_now(request):
    user = request.user
    product_id  = request.GET.get('prod_id') 
    product = Product.objects.get(id=product_id)
    qs = Cart.objects.filter(product=product)
    exists = qs.exists()
    if exists:
        return redirect('/cart')
    Cart(user=user, product=product).save()
    try:
        total_item = 0
        user = request.user
        if request.user.is_authenticated:
            total_item = len(Cart.objects.filter(user=request.user))
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
            totalamount = amount + shipping_amount
        return render(request, 'app/checkout_now.html', {'add':add, 'totalamount':totalamount, 'cart_items':cart_items, 'total_item':total_item})
    except:
        return render(request, 'app/not_product_found.html')



##=============================== Payment Done ========================================## 



##=============================== ProfileView ========================================## 
@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        total_item = 0
        if request.user.is_authenticated:
            total_item = len(Cart.objects.filter(user=request.user))
        form = CustomerPrfileForm()
        return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary', 'total_item':total_item})
    

##=============================== address ========================================## 
    def post(self, request):
        form = CustomerPrfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            location = form.cleaned_data['location']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr,name=name, location=location, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, 'Congratulations!! Profile Update Successfully!!')
            return redirect('/address')
        return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'})


##=============================== search ========================================## 
def search(request):
    query = request.GET['query']
    allproducttitle = Product.objects.filter(title__icontains=query)
    allproductContent = Product.objects.filter(description__icontains=query)
    allproductbrand = Product.objects.filter(brand__icontains=query)
    allproduct = allproducttitle.union(allproductContent, allproductbrand)
    return render(request, 'app/search.html' , {'allproduct':allproduct} )


@login_required
def checkout(request):
    try:
        total_item = 0
        user = request.user
        if request.user.is_authenticated:
            total_item = len(Cart.objects.filter(user=request.user))
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                totalamount = amount + shipping_amount
                
        return render(request, 'app/checkout.html', {'add':add, 'totalamount':totalamount, 'cart_items':cart_items, 'total_item':total_item})
    except:
        return render(request, 'app/not_product_found.html')



@login_required
def payment_done(request):
    try:
        user = request.user
        custid = request.GET.get('custid')
        customer = Customer.objects.get(id=custid)
        cart  = Cart.objects.filter(user=user)
        for c in cart:
            order = OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity)
            order.save()
            order_id = order.id
            cur_user_email = user.email
            totalamount = c.product.discounted_price * c.quantity + 70
            c.delete()

        param_dict={
            'MID': 'zgZiaS95597255328985',
            'ORDER_ID': str(order_id),
            'TXN_AMOUNT': str(totalamount),
            'CUST_ID': cur_user_email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL':'https://medicinex.herokuapp.com/handlepayment/',
        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return  render(request, 'app/paytm.html', {'param_dict': param_dict})
        # return redirect('orders')
    except:
        return render(request, 'app/house_not_found.html')


@csrf_exempt
def handlerequest(request):
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
            order_1 = (response_dict['ORDERID'])
            amount_1 = (response_dict['TXNAMOUNT'])
            # tsc_id_1 = (response_dict['TXNID'])

            email = EmailMessage('Transaction Fail',f"Order ID   :  {order_1} \nTotal Amount  :  {amount_1} \nTransaction ID  :   ", to=['visheshsolanki12345@gmail.com'])
            email.send()
    return render(request, 'app/paymentstatus.html', {'response': response_dict})


