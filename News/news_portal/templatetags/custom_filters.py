from django import template


register = template.Library()

bad_words = ['полёт', 'скорость', 'хоррор', 'скример', 'диссонанс', 'вопрос', 'чеченск']


@register.filter()
def filter_words(value):
    for i in range(len(bad_words)):
        if bad_words[i] in value:
            # фильтр слов с нижним регистром
            lo = bad_words[i].replace(bad_words[i][1:-1], '*' * len(bad_words[i][1:-1]))
            text = value.replace(bad_words[i], lo)
            # фильтр слов с Заглавной буквы
            ti = bad_words[i].title().replace(bad_words[i].title()[1:-1], '*' * len(bad_words[i].title()[1:-1]))
            text = text.replace(bad_words[i].title(), ti)
            # фильтр слов с ВЕРХНИМ РЕГИСТРОМ
            up = bad_words[i].upper().replace(bad_words[i].upper()[1:-1], '*' * len(bad_words[i].upper()[1:-1]))
            text = text.replace(bad_words[i].upper(), up)
            value = text
    return value


