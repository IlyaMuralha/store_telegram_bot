# конвертируем список с р[(5,),(8,),...] к [5,8,...]
def _convert(list_convert):
    return [itm[0] for itm in list_convert]


def total_coast(list_quantity, list_price):
    '''
    считает общую сумму заказа и возвращает результат
    '''
    order_total_coast = 0

    for ind, itm in enumerate(list_price):
        order_total_coast += list_quantity[ind]*list_price[ind]
        return order_total_coast


def total_quantity(list_quantity):
    '''
    считает общее количество заказанной единицы товара и возвращает результат
    '''
    order_total_quantity = 0

    for itm in list_quantity:
        order_total_quantity += itm

    return order_total_quantity


def get_total_coast(DB):
    '''
    возвращает общую стоимость товара
    '''
    all_product_id = DB.select_all_product_id()
    # получаем список стоимость по всем позициям заказа
    all_price = [DB.select_single_product_price(itm) for itm in all_product_id]
    # получаем список количества по всем позициям заказа
    all_quantity = [DB.select_order_quantity(itm) for itm in all_product_id]

    return total_coast(all_quantity, all_price)


def get_total_quantity(DB):
    '''
    возвращает общее количество товара
    '''
    all_product_id = DB.select_all_product_id()
    # получаем список количества по всем позициям заказа
    all_quantity = [DB.select_order_quantity(itm) for itm in all_product_id]

    return total_quantity(all_quantity)
