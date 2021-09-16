import json

from django.http     import JsonResponse
from django.views    import View

from products.models import *

"""""
 Django로 api를 더 자세하게 엔드포인트를 구하는 방법은 2가지가 있다.
 1. 함수형 view

urls.py

urlpattens = [
        path("", get_product)
]


def get_product(request):
        return JsonResponse({"message":"success"}, status=2000)
 
 2. class형 view - class형으로 하기를 권고함(좀더 명확하게 엔드포인트를 작성할 수 잇음)

urlpatterns = [
   path('', ProdctView.as_view())
]

"""""
#MenuView : 전체 메뉴의 정보를 가져오는 get함수와 메뉴정보를 등록하는 post함수가 있다.
#View클래스를 상속받는다. View는 장고에서 미리 만들어둔 클래스로 그냥 갖다 쓰면 된다.
#request는 프론트엔드에서 보내는 request를 받을 수 있는 파라미터이다. request메세지는 start line, headers, body 세가지로 구분되어 있다.
class MenuView(View):
    def get(self,request):
            menu = list(Menu.objects.create())
            #JsonResponse : dictionary형식의 응답(response)메시지를 json으로 변환한다.
            return JsonResponse({'data':menu}, status=200)
    def post(self,request):
            # 프론트에서 request body에 들어있는 정보는 json형식으로 들ㅇ러온다. 
            # 왜냐하면 프론트와 백에서 사용하는 언어가 다르므로 서로 정보를 주고받을 때는
            # json형식을 사용하기로 약속하였기 때문이다. 
            # 따라서 json.loads()는 들어온 정보(json)를 장고에서 사용할 수 있도록
            # 파이썬 dictionary형태로 변환하는 역할을 한다.
            data = json.loads(request.body)
            menu_name = Menu.objects.create(name=data['menu'])
            
            if not menu_name:
                return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400) 
            
            # filter(), exists()로 중복값을 막을 수 있다.
            # exists() : db에서 filter를 통해 원하는 조건의 데이터의 유무에 따라 true,false를 반환하는 메소드
            # 주의! get을 쓰면 찾는값이 없거나 찾는값이 2개이상이면 에러가 발생할 수 있다.
            if Menu.objects.filter(name=data['name']).exists():
                return JsonResponse({'message' : 'ALREADY_EXISTS'}, status=409)        
            
            
            Menu.objects.create(name=menu_name)
            return JsonResponse({'MESSAGE':'CREATED'}, status=201)
            
                    
# menu와 category는 onetomany관계!
class CategoryView(View):
    def get(self, request):
            menu= list(Category.objects.create())
            return 
    def post(self,request):
            data = json.loads(request.body)
            category_name=data.get('name', None)
            menu_name=data.get('menu_name', None)
        
            if not (category_name and menu_name):
                return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status=400)
            if Category.objects.filter(name=category_name).exists():
                return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status=400)
            if not Menu.objects.filter(name=menu_name).exists():
                return JsonResponse({'MESSAGE':'FOREIGN_KEY_DOES_NOT_EXIST'}, status=404)

            menu = Menu.objects.get(name=menu_name)
            Category.objects.create(
                    name=category_name,
                    menu=menu
            )
            return JsonResponse({'MESSAGE':'CREATED'}, status=201)
    
class ProductsView(View):
    def post(self, request):
        # json.loads를 하게되면 json형태의 dictionary타입으로 변환한다. 그렇게 되면 프론트가 요청한 데이터가 담겨져 나온다 
        # 왜 json형태로 변환하지? 파이썬(백)과 자바스크립트(프론트)랑 서로 소통하기 위해서 
        data = json.loads(request.body)
        menu = Menu.objects.create(name=data['menu'])
        category = Category.objects.create(
                name = data['category'],
                menu_id = menu.id
        )
        # Category의 menu는 foreign키로 지정되어 있기 때문에 menu만들면서 menu객체에 담아버리고
        # category의 menu에 연결 

        nutrition=Nutrition.objects.create(
                one_serving_kcal=120,
                sodium_mg=100,
                saturated_fat_g=100,
                sugars_g=100,
                protein_g=100,
                caffeine_mg=100
        )

        allergy=Allergy.objects.create(name=data['allergy_name'])
        
        product=Product.objects.create(
                name = data['product'],
                category_id = category.id,
                nutrition_id = nutrition.id
        )

        ProductAllergy.objects.create(
                allergy_id=allergy.id,
                product_id=product.id
        
        )        
        
        Image.objects.create(
                image_url=data['url'],
                product_id=product.id
                )
        
        return JsonResponse({'MESSAGE':'CREATED'}, status=201)

