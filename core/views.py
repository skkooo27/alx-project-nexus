from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the E-commerce Store")

def product_list(request):
    return HttpResponse("Here will be the list of products")

def product_detail(request, slug):
    return HttpResponse(f"Details for product: {slug}")

