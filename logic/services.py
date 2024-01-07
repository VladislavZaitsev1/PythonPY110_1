from store.models import DATABASE
import json
import os
from django.contrib.auth import get_user
def filtering_category(database: dict,
                       category_key: [int, str],
                       ordering_key: [None, str] = None,
                       reverse: bool = False):
    if category_key is not None:
        result = [value for value in database.values() if category_key == value['category']]  # TODO При помощи фильтрации в list comprehension профильтруйте товары по категории. Или можете использовать

    else:
        result = [value for value in database.values()]  # TODO Трансформируйте database в список словарей
    if ordering_key is not None:
        result.sort(key=lambda x: x[ordering_key], reverse=reverse)  # TODO Проведите сортировку result по ordering_key и параметру reverse
    return result

def view_in_cart(request) -> dict:
    if os.path.exists('cart.json'):  # Если файл существует
        with open('cart.json', encoding='utf-8') as f:
            return json.load(f)

    user = get_user(request).username  # Получаем авторизированного пользователя
    cart = {user: {'products': {}}}  # стало
    with open('cart.json', mode='x', encoding='utf-8') as f:  # Создаём файл и записываем туда пустую корзину
            json.dump(cart, f)

    return cart


def add_to_cart(request, id_product: str) -> bool:
    cart_users = view_in_cart(request)
    cart = cart_users[get_user(request).username]  # TODO Помните, что у вас есть уже реализация просмотра корзины,
        # поэтому, чтобы загрузить данные из корзины, не нужно заново писать код.

        # TODO Проверьте, а существует ли такой товар в корзине, если нет, то перед тем как его добавить - проверьте есть ли такой
        # id товара в вашей базе данных DATABASE, чтобы уберечь себя от добавления несуществующего товара.
    if id_product in DATABASE and id_product in cart['products']:
        cart['products'][id_product] += 1
    elif id_product in DATABASE and id_product not in cart['products']:
        cart['products'][id_product] = 1
    else:
        return False
    with open('cart.json', 'w', encoding='utf-8') as f:
            json.dump(cart_users, f)

    return True


def remove_from_cart(request, id_product: str) -> bool:
    cart_users = view_in_cart(request)
    cart = cart_users[get_user(request).username]
    if id_product not in cart['products']:
        return False
    else:
        cart['products'].pop(id_product)
    with open('cart.json', 'w', encoding='utf-8') as f:
            json.dump(cart_users, f)

            # TODO Помните, что у вас есть уже реализация просмотра корзины,
        # поэтому, чтобы загрузить данные из корзины, не нужно заново писать код.

        # TODO Проверьте, а существует ли такой товар в корзине, если нет, то возвращаем False.

        # TODO Если существует товар, то удаляем ключ 'id_product' у cart['products'].

        # TODO Не забываем записать обновленные данные cart в 'cart.json'

    return True

def add_user_to_cart(request, username: str) -> None:
    """
    Добавляет пользователя в базу данных корзины, если его там не было.

    :param username: Имя пользователя
    :return: None
    """
    cart_users = view_in_cart(request)  # Чтение всей базы корзин

    cart = cart_users.get(username)  # Получение корзины конкретного пользователя

    if not cart:  # Если пользователя до настоящего момента не было в корзине, то создаём его и записываем в базу
        with open('cart.json', mode='w', encoding='utf-8') as f:
            cart_users[username] = {'products': {}}
            json.dump(cart_users, f)



if __name__ == "__main__":


    test = [
        {'name': 'Клубника', 'discount': None, 'price_before': 500.0,
         'price_after': 500.0,
         'description': 'Сладкая и ароматная клубника, полная витаминов, чтобы сделать ваш день ярче.',
         'rating': 5.0, 'review': 200, 'sold_value': 700,
         'weight_in_stock': 400,
         'category': 'Фрукты', 'id': 2, 'url': 'store/images/product-2.jpg',
         'html': 'strawberry'},

        {'name': 'Яблоки', 'discount': None, 'price_before': 130.0,
         'price_after': 130.0,
         'description': 'Сочные и сладкие яблоки - идеальная закуска для здорового перекуса.',
         'rating': 4.7, 'review': 30, 'sold_value': 70, 'weight_in_stock': 200,
         'category': 'Фрукты', 'id': 10, 'url': 'store/images/product-10.jpg',
         'html': 'apple'}
    ]

    print(filtering_category(DATABASE, 'Фрукты', 'price_after', True) == test)  # True


