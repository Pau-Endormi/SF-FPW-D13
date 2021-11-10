from django import template

register = template.Library()

@register.filter(name='censor')

def censor(value, arg):
    obscenity = ['блять']
    list_value = value.split()
    for i in range(len(list_value)):
        if list_value[i] in obscenity:
            list_value[i] = arg
    return " ".join(list_value)
