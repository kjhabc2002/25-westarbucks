from django.shortcuts import render

# Create your views here.

import json

from django.http     import JsonResponse
from django.views    import View

from products.models import Menu, Category, Product


class ProductsView(View):
    def post(self, request):
        data = json.loads(request.body)
        menu = Menu.objects.create(name=data['menu'])
        category = Category.objects.create(
                name = data['category'],
                menu = menu
        )
        Product.objects.create(
                korean_name = data['product'],
                english_name = data['product'],
                description = data['product'],

                category = category,
                nutrition = nutrition,
                allergy = allergy
        )
        return JsonResponse({'MESSAGE':'CREATED'}, status=201)

