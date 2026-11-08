
from math import sqrt

# Еталонні характеристики квітів
# Висота, діаметр, червоний, жовтий, шипи
REFERENCES = {
    'Троянда': (80, 10, 1, 0, 1),
    'Тюльпан': (40, 7, 1, 0, 0),
    'Соняшник': (180, 25, 0, 1, 0)
}

# Масштабування характеристик
SCALES = (200, 30, 1, 1, 1)
THRESHOLD = 0.65


# Евклідова відстань
def distance(a, b):
    return sqrt(sum(
        ((x - y) / scale) ** 2
        for x, y, scale in zip(a, b, SCALES)
    ))


# Функція розпізнавання
def recognize(features):
    if len(features) != 5:
        raise ValueError(
            'Потрібно ввести рівно 5 характеристик.'
        )

    h, diameter, red, yellow, thorns = features

    if h <= 0 or diameter <= 0:
        raise ValueError(
            'Розміри мають бути додатними.'
        )

    if any(v not in (0, 1)
           for v in (red, yellow, thorns)):
        raise ValueError(
            'Якісні ознаки повинні бути 0 або 1.'
        )

    scores = {
        name: distance(features, ref)
        for name, ref in REFERENCES.items()
    }

    best = min(scores, key=scores.get)

    if scores[best] <= THRESHOLD:
        result = best
    else:
        result = 'Невідомий вид'

    return result, scores


# Контрольні приклади
def demo():
    cases = [
        ('Троянда', (78, 11, 1, 0, 1)),
        ('Тюльпан', (42, 7, 1, 0, 0)),
        ('Соняшник', (175, 24, 0, 1, 0)),
        ('Невідомий вид', (100, 15, 0, 0, 0))
    ]

    for expected, features in cases:
        result, scores = recognize(features)

        print('\nВхідні ознаки:', features)
        print('Очікувано:', expected)
        print('Результат:', result)

        for name, value in scores.items():
            print(f'{name}: {value:.3f}')

        assert result == expected

    # Перевірка помилки
    try:
        recognize((0, 10, 1, 0, 1))
    except ValueError as error:
        print('\nПомилка введення:', error)


# Основна програма
def main():
    print('РОЗПІЗНАВАННЯ КВІТІВ ЗА ОЗНАКАМИ')
    print('Еталони:', ', '.join(REFERENCES))

    print(
        'Для демонстраційних тестів '
        'натисніть Enter.'
    )

    raw = input(
        'Введіть 5 значень через пробіл: '
    ).strip()

    if not raw:
        demo()
        return

    try:
        values = tuple(
            float(v) for v in raw.split()
        )

        result, scores = recognize(values)

        for name, score in scores.items():
            print(
                f'{name}: відстань = {score:.3f}'
            )

        print(
            'Результат розпізнавання:', result
        )

    except ValueError as error:
        print('Помилка введення:', error)


if __name__ == '__main__':
    main()
