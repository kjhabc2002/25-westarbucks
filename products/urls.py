from django.urls   import path
from products.views import ProductsView
from products.views import MenuView

# 127.0.0.1:8000/product

# django_api.urls.py(Root URLconf)
# path('products', include('products.urls')),

urlpatterns = [
        path('/menu', MenuView.as_view()),
]
