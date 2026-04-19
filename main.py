"""
main.py — Punto de entrada
===========================
Instancia el servicio y despacha opciones del menú.
"""

from service import ServicioEstudiantes
from logic import leer_todos
from ui import (
    mostrar_menu, mostrar_todos, mostrar_tabla,
    flujo_crear, flujo_buscar, flujo_actualizar, flujo_eliminar,
)


def main() -> None:
    svc = ServicioEstudiantes()
    print(f"\nBienvenido  —  {svc.total} estudiante(s) cargado(s).")

    opciones = {
        "1": flujo_crear,
        "2": lambda s: mostrar_todos(s.leer_todos()),
        "3": lambda s: mostrar_tabla(s.leer_todos()),
        "4": flujo_buscar,
        "5": flujo_actualizar,
        "6": flujo_eliminar,
    }

    while True:
        mostrar_menu()
        opcion = input("  Opción (1-7): ").strip()

        if opcion == "7":
            print("\n  Hasta luego. 👋\n")
            break
        elif opcion in opciones:
            opciones[opcion](svc)
        else:
            print("  ⚠  Opción no válida.")


if __name__ == "__main__":
    main()
