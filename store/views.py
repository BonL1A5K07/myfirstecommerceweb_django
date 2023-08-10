from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.http import JsonResponse
import json
import datetime
from .utils import cookieCart,cartData,guestOrder
from django.db.models import Q

# Create your views here.
def store(request):
    if request.user.is_authenticated:
        # quan he 1-1 nen moi ghi nhu nay
        customer = request.user.customer
        order, create = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        # items = []
        # order = {'get_cart_total':0,'get_cart_items':0,'shipping':False}# return redirect('store:login')
        # cartItems = order['get_cart_items']
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']

    query = request.GET.get('query','')
    products = Product.objects.all()
    if query:
        products = products.filter(Q(name__icontains=query))

    return render(request,'store/store.html',{
        'products':products,
        'cartItems':cartItems,
        'query':query,
    })

def cart(request):

    if request.user.is_authenticated:
        # quan he 1-1 nen moi ghi nhu nay
        customer = request.user.customer
        order, create = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']

    return render(request,'store/cart.html',{
        'items':items,
        'order':order,
        'cartItems':cartItems,
    })

def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
        # return redirect('store:login')
    return render(request,'store/checkout.html',{
        'items':items,
        'order':order,
        'cartItems':cartItems,
    })

def login(request):
    return render(request,'store/login.html')

def updateItem(request):
    data = json.loads(request.body) # Get data from js
    productId = data['productId'] # Assign data to a variable
    action = data['action']

    print('action:',action)
    print('productId:',productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId) # Assign data which get from js to a variable id (db)
    order, created = Order.objects.get_or_create(customer=customer,complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order,product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse("Item was added to cart",safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        # total = float(data['form']['total'])
        # order.transaction_id = transaction_id
        # if total == order.get_cart_total:
        #     order.complete = True
        # order.save()
        # if order.shipping == True:
        #     ShippingAddress.objects.create(
        #         customer = customer,
        #         order = order,
        #         address = data['shipping']['address'],
        #         city = data['shipping']['city'],
        #         state = data['shipping']['state'],
        #         zipcode = data['shipping']['zipcode'],
        #     )
    else:
        # print ("User is not loggedin")
        # print ('COOKIES:',request.COOKIES)
        customer, order = guestOrder(request,data)

        
    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    if total == order.get_cart_total:
        order.complete = True
    order.save()
    if order.shipping == True:
        ShippingAddress.objects.create(
            customer = customer,
            order = order,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            zipcode = data['shipping']['zipcode'],
        )

    return JsonResponse("Payment .....",safe=False)