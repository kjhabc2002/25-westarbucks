from django.db import models


# Create your models here.
class Menu(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
          db_table = 'menus'

class Category(models.Model):
    name = models.CharField(max_length=20)
    menu = models.ForeignKey('Menu', on_delete=models.SET_NULL, null=true)

    class Meta:
          db_table = 'categories'

class Products(models.Model):
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    korean_name = models.CharField(max_length=50)
    english_name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)

    class Meta:
        db_table = 'products'

class AllergyDrink(models.Model):
    allergy = models.ForeignKey('Allergy', on_delete=models.SET_NULL, null=True)
    drink = models.ForeignKey('Drink', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'allergies_drinks'


class Allergy(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'allergies'

class Nutrition(models.Model):
    one_serving_kcal = models.DecimalField(max_digits=10, decimal_places=2)
    sodium_mg = models.DecimalField(max_digits=10, decimal_places=2)
    saturated_fat_g = models.DecimalField(max_digits=10, decimal_places=2)
    sugars_g = models.DecimalField(max_digits=10, decimal_places=2)
    protein_g = models.DecimalField(max_digits=10, decimal_places=2)
    caffeine_mg = models.DecimalField(max_digits=10, decimal_places=2)
    drink = models.ForeignKey('Drink', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'nutritions'

class Image(models.Model):
    image_url = models.URLField(max_length=2000)
    drink = models.ForeignKey('Drink', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'images


