from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .models import *
from django.contrib.auth.forms import UserCreationForm
from .forms import OrderForm, CreateUserForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login


# Create your views here.
def store(request):

     if request.user.is_authenticated:
          customer = request.user.customer
          order, created = Order.objects.get_or_create(customer=customer, complete=False)
          items= order.orderitem_set.all()
     else:
          items = []
          order = {'get_cart_total':0,'get_cart_items':0}
     products = Product.objects.all()
     context = {'products':products}
     return render(request, 'store/store.html', context)

def home(request):
     context = {}   
     return render(request, 'store/home.html', context)

def registerPage(request):
     form = CreateUserForm()
     
     
     if request.method == 'POST':
          form = CreateUserForm(request.POST)
          if form.is_valid():
               form.save()
               user = form.cleaned_data.get('username')
               messages.success(request, 'Account was created successfully for '+ user)
               
               return redirect('login')
          
          
     context = {'form':form}
     return render(request, 'store/register.html ', context) 

def loginPage(request):
     if request.method == 'POST':

          username = request.POST.get('username')
          password = request.POST.get('password')
          user = authenticate(request, username=username,password=password)
          
          if user is not None:

               login(request,user)
               return redirect('home')
          else:
               messages.info(request, 'Username OR Password Incorrect')
     context={}
     return render(request, 'store/login.html ', context)
     
          

def cart(request):
     if request.user.is_authenticated:
          customer = request.user.customer
          order, created = Order.objects.get_or_create(customer=customer, complete=False)
          items= order.orderitem_set.all()
     else:
          items = []
          order = {'get_cart_total':0,'get_cart_items':0}

     context = {'items':items,'order':order}
     return render(request, 'store/cart.html', context)

def checkout(request):
     if request.user.is_authenticated:
          customer = request.user.customer
          order, created = Order.objects.get_or_create(customer=customer, complete=False)
          items= order.orderitem_set.all()
     else:
          items = []
          order = {'get_cart_total':0,'get_cart_items':0}

     context = {'items':items,'order':order}
     return render(request, 'store/checkout.html', context)

def updateItem(request):
     data = json.loads(request.body)
     productId = data['productId']
     action = data['action']
     print('Action:', action)
     print('ProductId:', productId)

     customer = request.user.customer
     product = Product.objects.get(id=productId)
     order, created = Order.objects.get_or_create(customer=customer, complete=False)
     orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

     if action == 'add':
          orderItem.quantity = (orderItem.quantity + 1)
     elif action == 'remove':
          orderItem.quantity = (orderItem.quantity - 1)
          
     orderItem.save()
     
     if orderItem.quantity <= 0:
          orderItem.delete()

     return JsonResponse('Item was added', safe=False)