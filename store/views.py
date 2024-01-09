from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotFound
from .models import DATABASE
from django.http import HttpResponse
from logic.services import view_in_cart, add_to_cart, remove_from_cart, filtering_category
from django.shortcuts import redirect


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
        current_user = get_user(request).username
        data = view_in_cart(request)[current_user]
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
        result = add_to_cart(request, id_product)
        if result:
            return JsonResponse({"answer": "Продукт успешно добавлен в корзину"},
                                json_dumps_params={'ensure_ascii': False})

        return JsonResponse({"answer": "Неудачное добавление в корзину"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})


def cart_del_view(request, id_product):
    if request.method == "GET":
        result = remove_from_cart(request, id_product) # TODO Вызвать ответственную за это действие функцию
        if result:
            return JsonResponse({"answer": "Продукт успешно удалён из корзины"},
                                json_dumps_params={'ensure_ascii': False})
        else:
            return JsonResponse({"answer": "Неудачное удаление из корзины"},
                                status=404,
                                json_dumps_params={'ensure_ascii': False})



def coupon_check_view(request, name_coupon):
    # DATA_COUPON - база данных купонов: ключ - код купона (name_coupon); значение - словарь со значением скидки в процентах и
    # значением действителен ли купон или нет
    DATA_COUPON = {
        "coupon": {
            "value": 10,
            "is_valid": True},
        "coupon_old": {
            "value": 20,
            "is_valid": False},
    }
    if request.method == "GET":
       if name_coupon in DATA_COUPON:
           coupon = DATA_COUPON[name_coupon]
           return JsonResponse({
               'is_valid': coupon['is_valid'],
               'discount': coupon['value']
           })
       return HttpResponseNotFound('Неверный купон')


        # TODO Проверьте, что купон есть в DATA_COUPON, если он есть, то верните JsonResponse в котором по ключу "discount"
        # получают значение скидки в процентах, а по ключу "is_valid" понимают действителен ли купон или нет (True, False)

        # TODO Если купона нет в базе, то верните HttpResponseNotFound("Неверный купон")

def delivery_estimate_view(request):
        # База данных по стоимости доставки. Ключ - Страна; Значение словарь с городами и ценами; Значение с ключом fix_price
        # применяется если нет города в данной стране
    DATA_PRICE = {
            "Россия": {
                "Москва": {"price": 80},
                "Санкт-Петербург": {"price": 50},
                "fix_price": 100,
            },
        }
    if request.method == "GET":
        data = request.GET
        country = data.get('country')
        city = data.get('city')
        if country in DATA_PRICE:
            if city in DATA_PRICE[country]:
                return JsonResponse({'price': DATA_PRICE[country][city]['price']})
            else:
                return JsonResponse({'price': DATA_PRICE[country]['fix_price']})
        return HttpResponseNotFound('Неверные данные')
            # TODO Реализуйте логику расчёта стоимости доставки, которая выполняет следующее:
            # Если в базе DATA_PRICE есть и страна (country) и существует город(city), то вернуть JsonResponse со словарём, {"price": значение стоимости доставки}
            # Если в базе DATA_PRICE есть страна, но нет города, то вернуть JsonResponse со словарём, {"price": значение фиксированной стоимости доставки}
            # Если нет страны, то вернуть HttpResponseNotFound("Неверные данные")

def cart_buy_now_view(request, id_product):
    if request.method == "GET":
        result = add_to_cart(request, id_product)
        if result:
            return redirect("store:cart_view")
        return HttpResponseNotFound("Неудачное добавление в корзину")

def cart_remove_view(request, id_product):
    if request.method == "GET":
        result = remove_from_cart(request, id_product)  # TODO Вызвать функцию удаления из корзины
        if result:
            return redirect('store:cart_view')  # TODO Вернуть перенаправление на корзину

        return HttpResponseNotFound("Неудачное удаление из корзины")