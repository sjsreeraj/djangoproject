from django.shortcuts import render
from shop.models import Products
from cart.models import Cart,Account,Order
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def cartview(request):
    total=0
    u=request.user
    cart=Cart.objects.filter(user=u)
    for i in cart:
        total+=i.quantity*i.product.price
    return render(request,'cart.html',{'c':cart,'total':total})
@login_required
def addtocart(request,n):
    p=Products.objects.get(name=n)
    u=request.user
    try:
        cart=Cart.objects.get(user=u,product=p)
        if(p.stock > 0):
            cart.quantity+=1
            cart.save()
            p.stock-=1
            p.save()

    except:
        if(p.stock > 0):
               cart=Cart.objects.create(product=p,user=u,quantity=1)
               cart.save()
               p.stock-=1
               p.save()


    return cartview(request)

@login_required
def cart_remove(request,n):
    p=Products.objects.get(name=n)
    u=request.user
    try:
        cart=Cart.objects.get(product=p,user=u)
        if(cart.quantity>1):
            cart.quantity-=1
            cart.save()
            p.stock+=1
            p.save()
        else:
            cart.delete()
            p.stock+=1
            p.save()

    except:
        pass

    return cartview(request)
@login_required
def cart_delete(request,n):
    p=Products.objects.get(name=n)
    u=request.user

    try:
        cart=Cart.objects.get(product=p,user=u)

        cart.delete()
        p.stock+=cart.quantity
        p.save()
    except:
        pass

    return cartview(request)
@login_required
def orderform(request):
    if request.method=="POST":
        a=request.POST['a']
        p=request.POST['p']
        n=request.POST['n']


        u=request.user
        cart=Cart.objects.filter(user=u)


        total=0
        for i in cart:
            total+=i.quantity*i.product.price


        try:
            ac=Account.objects.get(acctnum=n)
            if(ac.amount >= total):
                ac.amount=ac.amount-total
                ac.save()
                for i in cart:
                    o=Order.objects.create(user=u,product=i.product,address=a,phone=p,no_of_items=i.quantity,order_status="paid")
                    o.save()
                cart.delete()
                msg="order placed successfully"
                return render(request,'orderdetail.html',{'msg':msg})
            else:
                msg="insufficient balance"
                return render(request,'orderdetail.html',{'msg':msg})

        except:
            pass

    return render(request,'orderform.html')
@login_required
def orderview(request):
    u=request.user
    o=Order.objects.filter(user=u)
    return render(request,'orderview.html',{'o':o,'u':u.username})













