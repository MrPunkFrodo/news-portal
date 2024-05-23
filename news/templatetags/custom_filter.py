from django import template

register = template.Library()

CENSOR_WORD = ['доктор', 'солей', 'Ситуаций']


@register.filter()
def censor(value):
    if not isinstance(value, str):
        raise ValueError("Неверное значение")

    def replace_with_stars(word):
        return word[0] + '*' * (len(word) - 1)
    for word in CENSOR_WORD:
        value = value.replace(word, replace_with_stars(word))

    return value
