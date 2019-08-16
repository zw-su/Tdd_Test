# coding = utf-8

from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item, List
from django.core.exceptions import ValidationError
# Create your views here.


def home_page(request):
    return render(request, 'home.html')


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    # items = Item.objects.filter(list_id=list_)
    return render(request, 'list.html', {'list': list_})


def new_list(request):
    list_ = List.objects.create()
    item = Item(text=request.POST['item_text'], list_id=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        error = '你不能输入一个空的待办事项'
        return render(request, 'home.html', {'error':error})
    return redirect(f'/lists/{list_.id}/')


def add_item(request, list_id):
    list_ = List.objects.get(id=int(list_id))
    Item.objects.create(text=request.POST['item_text'], list_id=list_)
    return redirect(f'/lists/{list_.id}/')
