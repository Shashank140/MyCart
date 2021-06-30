from django.shortcuts import render
from .models import Product, Contact, Orders, OrderUpdate
from math import ceil
import json
# from django.views.decorators.csrf import csrf_exempt

# import logger
import logging
logger = logging.getLogger(__name__)

# Create your views here.
from django.http import HttpResponse

def index(request):
    # products = Product.objects.all()
    # print(products)
    # n = len(products)
    # nSlides = n//4 + ceil((n/4)-(n//4))

    allProds = []
    catprods = Product.objects.values('category', 'id')
    category = {item['category'] for item in catprods}
    for cat in category:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    # params = {'no_of_slides':nSlides, 'range': range(1,nSlides),'product': products}
    # allProds = [[products, range(1, nSlides), nSlides],
    #             [products, range(1, nSlides), nSlides]]
    params = {'allProds':allProds}
    return render(request, 'shop/index1.html', params)

def searchApp(query, item):
    ''':return true only if query matches item
    for complex search use tfidfvectorizer or universal sentence encoder'''
    if query in item.product_name or query in item.category.lower() or query in item.desc or query in item.sub_category.lower():
        return True
    else:
        return False

def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    category = {item['category'] for item in catprods}
    for cat in category:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchApp(query, item)]
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if (len(prod) != 0):
            allProds.append([prod, range(1, nSlides), nSlides])

        params = {'allProds': allProds, "msg" : ""}
        if len(allProds) == 0 or len(query)<3:
            params = {'msg' : "Please make sure to enter valid query"}
    return render(request, 'shop/search.html', params)

def about(request):
    return render(request, 'shop/about.html')

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name','')
        email = request.POST.get('email','')
        phone = request.POST.get('phone','')
        desc = request.POST.get('desc','')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()

    return render(request, 'shop/contact.html')

def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps({"status":"success", "updates":updates, "itemsJson" : order[0].items_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')

    return render(request, 'shop/tracker.html')

def productView(request, myid):
    # Fetching product using id
    product = Product.objects.filter(id=myid)
    print(product)
    return render(request, 'shop/productView.html', {'product':product[0]})

def checkout(request):
    if request.method == "POST":
        items_json = request.POST.get('itemsJson','')
        name = request.POST.get('name','')
        amount = request.POST.get('amount','')
        email = request.POST.get('email','')
        phone = request.POST.get('phone','')
        address = request.POST.get('address1','') + request.POST.get('address2','')
        city = request.POST.get('city','')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code','')
        order = Orders(items_json=items_json, name=name, amount=amount, email=email, phone=phone, address=address, city=city, state=state, zip_code=zip_code)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        return render(request, 'shop/checkout.html', {'thank':thank, 'id':id})
    #Here we request paytm to transfer amount

    return render(request, 'shop/checkout.html')

#@csrf_exempt
#def handlerequest(request):
    # post request from paytm
 #   pass


