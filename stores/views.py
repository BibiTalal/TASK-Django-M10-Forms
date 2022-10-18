from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from multiprocessing import context
from stores import models
from .forms import StoreItemForm
from .models import StoreItem
from django.http import Http404
from django.shortcuts import (get_object_or_404, render, HttpResponseRedirect)
from django.template import loader


def get_store_items(request: HttpRequest) -> HttpResponse:
    store_items: list[models.StoreItem] = list(models.StoreItem.objects.all())
    context = {
        "store_items": store_items,
    }
    return render(request, "store_item_list.html", context)


def create_store_item(request):
    form = StoreItemForm()
    if request.method == "POST":
        form = StoreItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("store-item-list")

    context = {"form": form}
    return render(request, "create_store_item.html", context)


def update_store_item(request, item_id):
    store_item = StoreItem.objects.get(id=item_id)
    form = StoreItemForm(instance=store_item)
    if request.method == "POST":
        form = StoreItemForm(request.POST, instance=store_item)
        if form.is_valid():
            form.save()
            return redirect("store-item-list")
    context = {
        "form": form,
        "store_item": {
            "id": store_item.id
        }}
    return render(request, "update_store_item.html", context)


def delete_store_item(request, item_id):
    try:
        store_item = StoreItem.objects.get(id=item_id).delete()
    # store_item.delete()

    except StoreItem.DoesNotExist:
        store_item = None
    #     raise Http404("Item does not exist")
    #     return redirect("store-item-list")
    return render(request, "delete_store_item.html", {"store_item": store_item})
    # return render(request, "delete_store_item.html")
