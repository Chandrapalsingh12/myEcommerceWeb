from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Contact, Orders, OrderUpdate
from math import ceil
import json
from django.views.decorators.csrf import csrf_exempt
from Paytm import Checksum

MERCHANT_KEY = 'kbzk1DSbJiV_O3p5'
def index(request):
    allProds = []
    catProd = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catProd}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nslide = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nslide), nslide])
    my = {'allProds': allProds}
    return render(request, 'shop/index.html', my)

def searchMatch(query, item):
    if query in item.desc or query in item.product_name or query in item.category:
        return True
    else:
        False


    return False

def search(request):
    query = request.GET.get('search')
    allProds = []
    catProd = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catProd}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]
        n = len(prod)
        nslide = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) !=0:
            allProds.append([prod, range(1, nslide), nslide])
    my = {'allProds': allProds, "msg": ""}
    if len(allProds) == 0 or len(query) < 4:
        my = {'msg': "Please make sure to enter relevant search query"}
    return render(request, 'shop/search.html', my)



def about(request):
    return render(request, "shop/about.html")

def contact(request):
    thank = False
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        message = request.POST.get('message', '')
        print(name, email, phone, message)
        contact = Contact(name=name, email=email, phone=phone, message=message)
        contact.save()
        thank = True
    return render(request, "shop/contact.html",{'thank': thank})

def tracker(request):
    if request.method == "POST":
        orderid = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderid, email=email)
            if len(order) > 0:
                update = OrderUpdate.objects.filter(order_id=orderid)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps({"status": "success", "updates": updates, "itemsJson": order[0].items_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status": "noitems"}')
        except Exception as e:
            return HttpResponse('{"status": "Error"}')

    return render(request, 'shop/tracker.html')

def product(request, myid):
    #Fetch the Product

    product = Product.objects.filter(id=myid)
    return render(request, "shop/product.html", {"product": product[0]})

def checkout(request):
    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address', '')
        address2 = request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Orders(items_json=items_json, name=name, amount=amount,  email=email, address=address, address2=address2, city=city,
                       state=state, zip_code=zip_code, phone=phone)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        # return render(request, 'shop/checkout.html', {'thank':thank, 'id': id})
        # Request paytm to transfer the amount on your account after payment by user
        param_dict = {
            'MID': 'WorldP64425807474247',
            'ORDER_ID': str(order.order_id),
            'TXN_AMOUNT': str(amount),
            'CUST_ID': email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': 'http://127.0.0.1:8000/shop/handelrequest/',
        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request, 'shop/paytm.html', {'param_dict': param_dict})

    return render(request, 'shop/checkout.html')

@csrf_exempt
def handlerequest(request):
    # Paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] =='01':
            print('Order Successful')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
        return render(request, 'shop/paymentstatus.html', {'response': response_dict})

