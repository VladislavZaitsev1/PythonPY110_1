from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotFound
from .models import DATABASE
from django.http import HttpResponse
from logic.services import view_in_cart, add_to_cart, remove_from_cart, filtering_category


def products_view(request):
    if request.method == "GET":
        id = request.GET.get('id')
        if id:
            if id in DATABASE:
                return JsonResponse(DATABASE[id], json_dumps_params={'ensure_ascii': False, 'indent': 4})
            return HttpResponseNotFound('Данного  продукта нет в базе данных')
        category_key = request.GET.get('category')
        ordering_key = request.GET.get('ordering')
        if ordering_key:
            if request.GET.get('reverse') in ['true', 'TRUE', 'True']:
                data = filtering_category(DATABASE, category_key, ordering_key, True)
            else:
                data = filtering_category(DATABASE, category_key, ordering_key)
        else:
            data = filtering_category(DATABASE, category_key)

        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False,
                                                                              'indent': 4})
# Create your views here.

def products_page_view(request, page):
    if request.method == "GET":
        if isinstance(page, str):
            for data in DATABASE.values():
                if data['html'] == page:
                    with open(f'store/products/{page}.html', 'r', encoding='utf8') as f:
                        data = f.read()
                    return HttpResponse(data)
        elif isinstance(page, int):
            if str(page) in DATABASE:
                with open(f'store/products/{DATABASE[str(page)]["html"]}.html', 'r', encoding='utf8') as f:
                    data = f.read()
                return HttpResponse(data)
        # Если за всё время поиска не было совпадений, то значит по данному имени нет соответствующей
        # страницы товара и можно вернуть ответ с ошибкой HttpResponse(status=404)
        return HttpResponse(status=404)


def shop_view(request):
    if request.method == "GET":
        category_key = request.GET.get("category")
        if ordering_key := request.GET.get("ordering"):
            if request.GET.get("reverse") in ('true', 'True'):
                data = filtering_category(DATABASE, category_key, ordering_key,
                                          True)
            else:
                data = filtering_category(DATABASE, category_key, ordering_key)
        else:
            data = filtering_category(DATABASE, category_key)
        return render(request, 'store/shop.html', context={'products': data,
                                                           'category': category_key})


def cart_view(request):
    if request.method == "GET":
        data = view_in_cart()
        if request.GET.get('format') in ('json', 'JSON'):
              # TODO Вызвать ответственную за это действие функцию
            return JsonResponse(data, json_dumps_params={'ensure_ascii': False, 'indent': 4})

        products = []
        for product_id, quantity in data['products'].items():
            product = DATABASE.get(product_id)
            product['quantity'] = quantity
            product["price_total"] = f"{quantity * product['price_after']:.2f}"
            products.append(product)
        return render(request, "store/cart.html", context={'products': products})


def cart_add_view(request, id_product):
    if request.method == "GET":
        result = add_to_cart(id_product) # TODO Вызвать ответственную за это действие функцию
        if result:
            return JsonResponse({"answer": "Продукт успешно добавлен в корзину"},
                                json_dumps_params={'ensure_ascii': False})

        return JsonResponse({"answer": "Неудачное добавление в корзину"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})


def cart_del_view(request, id_product):
    if request.method == "GET":
        result = remove_from_cart(id_product) # TODO Вызвать ответственную за это действие функцию
        if result:
            return JsonResponse({"answer": "Продукт успешно удалён из корзины"},
                                json_dumps_params={'ensure_ascii': False})
        else:
            return JsonResponse({"answer": "Неудачное удаление из корзины"},
                                status=404,
                                json_dumps_params={'ensure_ascii': False})

