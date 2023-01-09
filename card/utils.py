import random


# Валидация номера банковской карты по алгоритму Луна
def validate_card_number(card_number):
    card_number = str(card_number)  # преобразуем в строку для удобства
    card_number = card_number[::-1]  # разворачиваем строку
    card_number = list(card_number)  # преобразуем в список для удобства
    card_number = [int(i) for i in card_number]  # преобразуем в список целых чисел   
    for i in range(1, len(card_number), 2):
        card_number[i] = card_number[i] * 2
        if card_number[i] > 9:
            card_number[i] = card_number[i] - 9
    if sum(card_number) % 10 == 0:
        return True  # номер карты валидный
    else:
        return False  # номер карты не валидный


def generate_card_number():
    # генерирует рандомный номер карты
    card_number = random.randint(1000000000000000, 9999999999999999)  # генерируем рандомный номер карты
    if validate_card_number(card_number):  # проверяем валидность номера карты
        return card_number  # возвращаем номер карты
    else:
        return generate_card_number()  # если номер карты не валидный, генерируем новый
