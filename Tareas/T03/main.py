from sistemas import Red
from menu import Menu


path = 'bd/large/'
red = Red(path)

menu = Menu(red)
menu.menu_principal()

