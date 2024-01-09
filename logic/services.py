import json
import os



from store.models import DATABASE
from django.contrib.auth import get_user



def filtering_category(database: dict,
                       category_key: [int, str],
                       ordering_key: [None, str] = None,
                       reverse: bool = False):

    if category_key is not None:
        result = [good for good in database.values() if good['category'] == category_key]
        # TODO При помощи фильтрации в list comprehension профильтруйте товары по категории. Или можете использовать
        # обычный цикл или функцию filter
    else:
        result = [good for good in database.values()]
    # TODO Трансформируйте database в список словарей
    if ordering_key is not None:
        result = sorted(result, key=lambda x: x[ordering_key], reverse=reverse)
        # TODO Проведите сортировку result по ordering_key и параметру reverse

    return result


def view_in_cart(request) -> dict:
    if os.path.exists('cart.json'):
        with open('cart.json', encoding='utf-8') as f:
            return json.load(f)
    user = get_user(request).username
    cart = {user: {'products': {}}}
    with open('cart.json', mode='x', encoding='utf-8') as f:
        json.dump(cart, f)

    return cart


def add_to_cart(request, id_product: str) -> bool:
    cart_users = view_in_cart(request)
    cart = cart_users[get_user(request).username]
    if id_product not in DATABASE:
        return False
    if id_product not in cart['products']:
        cart['products'][id_product] = 1
    else:
        cart['products'][id_product] += 1
    with open('cart.json', mode='w', encoding='utf-8') as f:
        json.dump(cart_users, f)

    return True


def remove_from_cart(request, id_product: str) -> bool:
    cart_users = view_in_cart(request)
    cart = cart_users[get_user(request).username]

    if id_product not in cart['products']:
        return False
    cart['products'].pop(id_product)
    with open('cart.json', mode='w', encoding='utf-8') as f:
        json.dump(cart_users, f)

    return True


def add_user_to_cart(request, username: str) -> None:
    cart_users = view_in_cart(request)
    cart = cart_users.get(username)
    if not cart:
        with open('cart.json', mode='w', encoding='utf-8') as f:
            cart_users[username] = {'products': {}}
            json.dump(cart_users, f)


def add_user_to_wishlist(request, username: str) -> None:
    wishlist_users = view_in_wishlist(request)
    wishlist = wishlist_users.get(username)
    if not wishlist:
        with open('wishlist.json', mode='w', encoding='utf-8') as f:
            wishlist_users[username] = {'products': []}
            json.dump(wishlist_users, f)


def view_in_wishlist(request) -> dict:
    if os.path.exists('wishlist.json'):
        with open('wishlist.json', encoding='utf-8') as f:
            return json.load(f)

    user = get_user(request).username
    wishlist = {user: {'products': []}}
    with open('wishlist.json', mode='x', encoding='utf-8') as f:
        json.dump(wishlist, f)

    return wishlist


def add_to_wishlist(request, id_product: str) -> bool:
    wishlist_users = view_in_wishlist(request)
    wishlist = wishlist_users[get_user(request).username]
    if id_product not in DATABASE:
        return False
    if id_product not in wishlist['products']:
        wishlist['products'].append(id_product)
    with open('wishlist.json', mode='w', encoding='utf-8') as f:
        json.dump(wishlist_users, f)

    return True


def remove_from_wishlist(request, id_product: str) -> bool:

    wishlist_users = view_in_wishlist(request)
    wishlist = wishlist_users[get_user(request).username]
    if id_product not in wishlist['products']:
        return False
    wishlist['products'].remove(id_product)
    with open('wishlist.json', mode='w', encoding='utf-8') as f:
        json.dump(wishlist_users, f)
        return True