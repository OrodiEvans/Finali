import json

from django.contrib.sites import requests
from django.http import HttpResponse
from django.shortcuts import render, redirect
from requests.auth import HTTPBasicAuth

from EcommerceApp.credentials import MpesaAccessToken, LipanaMpesaPpassword
from EcommerceApp.form import ProductForm
from EcommerceApp.models import User, Product


# Create your views here.
def contact(request):
    return render(request, 'contact.html')


def index(request):
    if request.method == 'POST':
        if User.objects.filter(username=request.POST['username'], password=request.POST['password']).exists():
            user = User.objects.get(username=request.POST['username'], password=request.POST['password'])
            return render(request, 'index.html', {'user': user})
        else:
            return render(request, 'index.html')
    else:
        return render(request, 'index.html')


def login(request):
    return render(request, 'login.html')


def signup(request):
    if request.method == 'POST':
        user = User(username=request.POST['username'],
                    email=request.POST['email'],
                    password=request.POST['password'])
        user.save()
        return redirect('/')
    else:
        return render(request, 'signup.html')


def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})


def upload_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()

    return render(request, 'upload_product.html', {'form': form})


def pay(request):
    return render(request, 'pay.html')


def token(request):
    consumer_key = '77bgGpmlOxlgJu6oEXhEgUgnu0j2WYxA'
    consumer_secret = 'viM8ejHgtEmtPTHd'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(
        consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token["access_token"]

    return render(request, 'token.html', {"token": validated_mpesa_access_token})


def stk(request):
    if request.method == "POST":
        phone = request.POST['phone']
        amount = request.POST['amount']
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        request = {
            "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
            "Password": LipanaMpesaPpassword.decode_password,
            "Timestamp": LipanaMpesaPpassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": LipanaMpesaPpassword.Business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
            "AccountReference": "Eva Fresh",
            "TransactionDesc": "Product Charges"
        }
        response = requests.post(api_url, json=request, headers=headers)
        return HttpResponse("Request Success")
