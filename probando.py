def suma_total(*args):
    sumar = sum(args)
    return sumar

# Prueba la función
print(suma_total(2, 3, 5))  # Debe devolver 10
print(suma_total(1, 2))     # Debe devolver 3



def mostrar_info_personal(**kwargs):
    for clave, valor in kwargs.items():
        print (f"{clave}: {valor}")

# Prueba la función
mostrar_info_personal(nombre="Carlos", edad=30, ciudad="Lima", apellido='Kyle')
# Debe imprimir:
# nombre: Carlos
# edad: 30
# ciudad: Lima


def filtrar_productos(*args, **kwargs):
    pass  # Tu código aquí
# Prueba la función
productos = ['laptop', 'celular', 'reloj', 'tablet']
filtrar_productos(*productos, tipo='electronico', precio_max=500)
