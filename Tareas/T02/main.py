from dccasino import DCCasino


print('Ingrese el tiempo de simulación del casino en minutos')
tiempo = input('Tiempo: ')
if not tiempo.isdigit():
    print('El tiempo debe ser un número\nFin')


else:
    casino = DCCasino(int(tiempo))
    casino.simulacion()