from django.shortcuts import render
from shop.models import Products
from django.db.models import Q

# Create your views here.
def search(request):
    b=None
    q=""
    if(request.method=="POST"):
           q=request.POST['q']
           if q:
              b=Products.objects.filter(Q(name__icontains=q)|Q(desc__icontains=q))

    return render(request,'search.html',{'q':q,'b':b})