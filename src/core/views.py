from django.http import HttpResponse
from django.shortcuts import render


def saludar(request):
    return HttpResponse('¡Hola Django!')


def saludar_con_etiqueta(request):
    return HttpResponse('<h1> Este es el título de mi App </h1>')


def saludar_con_parametros(request, nombre: str, apellido: str):
    nombre = nombre.capitalize()
    apellido = apellido.capitalize()
    return HttpResponse(f'{apellido}, {nombre}')


def index(request):
    from datetime import datetime

    año_actual = datetime.now().year
    context = {'año': año_actual}
    return render(request, 'core/index.html', context)


def tirar_dado(request):
    from datetime import datetime
    from random import randint

    tiro_de_dado = randint(1, 6)

    if tiro_de_dado == 6:
        mensaje = f'Has tirado el 🎲 y has sacado ¡{tiro_de_dado}! 😊 ✨ Ganaste ✨'
    else:
        mensaje = f'Has tirado el 🎲 y has sacado ¡{tiro_de_dado}! 😒 Sigue intentando. Presiona F5'

    datos = {
        'title': 'Tiro de Dados',
        'mensaje': mensaje,
        'fecha': datetime.now().strftime('%H:%M:%S.%f'),
    }
    return render(request, 'core/dados.html', context=datos)


def ejercicio_1(request):
    nombre = 'Louis'
    apellido = 'Van Beethoven'
    return render(request, 'core/ejercicio-1.html', {'nombre': nombre, 'apellido': apellido})


def ver_notas(request):
    lista_notas = [10, 8, 3, 7, 4, 5, 8]
    return render(request, 'core/notas.html', {'notas': lista_notas})


def ejercicio_2(request):
    usuarios = [
        {'nombre': 'juan', 'email': 'juan@django'},
        {'nombre': 'santi', 'email': 'juan@django'},
        {'nombre': 'agustín', 'email': 'juan@django'},
    ]
    return render(request, 'core/ejercicio-2.html', {'usuarios': usuarios})
