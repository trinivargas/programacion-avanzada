import os


def buscar_archivo(name, cwd=os.getcwd()):
    # sacado de https://stackoverflow.com/questions/1724693/find-a-file-in-python
    for root, dirs, files in os.walk(cwd):
        if name in files:
            return os.path.join(root, name)


def leer_archivo(path):
    bytes = []
    with open(path, 'rb') as file:
        for byte in file.read():
            bytes.append(byte)
    numeros = [bin(b)[2:].zfill(7) for b in bytes]
    listos = []
    i = 0
    while i < len(bytes):
        n = numeros[i] + numeros[i + 1]
        j = n.find('1')
        listos.append(n[j + 1:])
        i += 2
    return listos


def decodificar(bits):
    posiciones = []
    i = 0
    lugar = ''
    while 2 ** i - 1 < len(bits):
        posiciones.append(2 ** i - 1)
        i += 1

    for i in posiciones:
        b = bits[i:]
        s = ''
        j = 0
        n = 0
        while j < len(b) - 2:
            if not n % 2:
                s += b[j: j + i]
            j += i
        if s.count('1') % 2:
            lugar += '1'
        else:
            lugar += '0'
    if not '1' in posiciones:
        return bits
    lugar = chr(lugar[::-1])
    if bits[lugar] == '0':
        bits[lugar] = '1'
    else:
        bits[lugar] = '0'
    return bits



def escribir_archivo(ruta, chunks):
    pass


# Aquí puedes crear todas las funciones extra que requieras.


if __name__ == "__main__":
    nombre_archivo_de_pista = "himno.shrek"
    ruta_archivo_de_pista = buscar_archivo(nombre_archivo_de_pista)

    chunks_corruptos_himno = leer_archivo(ruta_archivo_de_pista)

    chunks_himno = [decodificar(chunk) for chunk in chunks_corruptos_himno]

    '''nombre_ubicacion_himno = "himno.png"
    escribir_archivo(nombre_ubicacion_himno, chunks_himno)'''
