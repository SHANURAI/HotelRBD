from django import template

register = template.Library()
COLUMN_TRANSLATIONS = {
    'Room_ID': 'Идентификатор комнаты',
    'Type': 'Тип',
    'cost_per_night': 'Стоимость за ночь',
    'Image_URL': 'Изображение',

    'Client_ID': 'Идентификатор клиента',
    'Fullname': 'Полное имя',
    'Year_of_birth': 'Год рождения',
    'Gender': 'Пол',
    'Username': 'Имя пользователя',

    'Service_ID': 'Идентификатор услуги',
    'Name': 'Название',
    'Cost': 'Стоимость',
    'Description': 'Описание',

    'Post_ID': 'Идентификатор должности',
    'Salary': 'Зарплата',

    'Staff_ID': 'Идентификатор сотрудника',

    'Booking_ID': 'Идентификатор бронирования',
    'Check_in_date': 'Дата заезда',
    'Check_out_date': 'Дата выезда',
    'Count_of_nights': 'Количество ночей',
    'Total_booking_cost': 'Общая стоимость бронирования',

    'Count_of_services': 'Количество услуг',
    'Total_service_cost': 'Общая стоимость услуг',
}

TABLE_TRANSLATIONS = {
    'Rooms': 'Комнаты',
    'Clients': 'Клиенты',
    'Services': 'Услуги',
    'Posts': 'Должности',
    'Staff': 'Персонал',
    'Bookings': 'Бронирования',
    'Provided_Services': 'Предоставленные услуги',
}

@register.filter
def translate_column(value):
    from .custom_filters import COLUMN_TRANSLATIONS
    return COLUMN_TRANSLATIONS.get(value, value)  
#Если нет перевода, вернёт оригинал

@register.filter
def zip_lists(list1, list2):
    return zip(list1, list2)

@register.filter(name='startswith')
def startswith(value, arg):
    if isinstance(value, str):
        return value.startswith(arg)
    return False

@register.filter
def translate_table(value):
    return TABLE_TRANSLATIONS.get(value, value)