# coding = utf-8

from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item, List

# Create your views here.


def home_page(request):
    return render(request, 'home.html')


def view_list(request, list_id):
    list_ = List.objects.get(list_id=list_id)
    items = Item.objects.filter(list_id=list_)
    return render(request, 'list.html', {'items': items})


def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list_id=list_)
    return redirect(f'/lists/{list_.list_id}/')
