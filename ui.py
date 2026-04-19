"""
ui.py — Capa de presentación
==============================
Solo imprime y pide input.
Importa ÚNICAMENTE service.py — desacoplada de data y logic.
"""

from service import ServicioEstudiantes
from logic import ResumenEstudiante


# ── Presentación ──────────────────────────────────────────────────────────────

def _estado(aprobado: bool) -> str:
    return "APROBADO ✅" if aprobado else "REPROBADO ❌"


def mostrar_tarjeta(d: ResumenEstudiante) -> None:
    notas_str = ", ".join(str(int(n) if n == int(n) else n) for n in d["notas"])
    print(f"\n  Nombre  : {d['nombre']}")
    print(f"  Notas   : [{notas_str}]")
    print(f"  Promedio: {d['promedio']:.2f}  →  {_estado(d['aprobado'])}")


def mostrar_tabla(resumen: list[ResumenEstudiante]) -> None:
    print("\n--- Resumen de Promedios ---")
    if not resumen:
        print("  (No hay estudiantes registrados)")
        return
    print(f"\n  {'Nombre':<20} {'Promedio':>10}  Estado")
    print("  " + "─" * 44)
    for d in resumen:
        print(f"  {d['nombre']:<20} {d['promedio']:>10.2f}  {_estado(d['aprobado'])}")
    print()


def mostrar_todos(resumen: list[ResumenEstudiante]) -> None:
    print("\n--- Listado Completo ---")
    if not resumen:
        print("  (No hay estudiantes registrados)")
        return
    for d in resumen:
        mostrar_tarjeta(d)
    print()


def mostrar_menu() -> None:
    print("\n" + "═" * 38)
    print("   SISTEMA DE GESTIÓN DE NOTAS  v4")
    print("═" * 38)
    print("  1. Agregar estudiante       (Create)")
    print("  2. Ver todos los estudiantes (Read)")
    print("  3. Ver tabla de promedios    (Read)")
    print("  4. Buscar estudiante         (Read)")
    print("  5. Actualizar notas         (Update)")
    print("  6. Eliminar estudiante      (Delete)")
    print("  7. Salir")
    print("═" * 38)


# ── Entrada ───────────────────────────────────────────────────────────────────

def pedir_nombre(prompt: str = "  Nombre: ") -> str:
    return input(prompt).strip()


def pedir_notas() -> list[float]:
    notas: list[float] = []
    print("  Ingresa notas (escribe 'fin' para terminar):")
    while True:
        entrada = input(f"    Nota {len(notas) + 1}: ").strip()
        if entrada.lower() == "fin":
            break
        try:
            nota = float(entrada)
            notas.append(nota) if 0 <= nota <= 100 else print("    ⚠  Entre 0 y 100.")
        except ValueError:
            print("    ⚠  Número inválido o escribe 'fin'.")
    return notas


def confirmar(pregunta: str) -> bool:
    return input(f"  {pregunta} [s/n]: ").strip().lower() == "s"


# ── Flujos CRUD (llaman solo a service) ───────────────────────────────────────

def flujo_crear(svc: ServicioEstudiantes) -> None:
    print("\n--- Agregar Estudiante ---")
    nombre = pedir_nombre()
    notas  = pedir_notas()
    ok, msg = svc.crear(nombre, notas)
    print(f"\n  {'✅' if ok else '⚠ '} {msg}")


def flujo_buscar(svc: ServicioEstudiantes) -> None:
    print("\n--- Buscar Estudiante ---")
    datos = svc.leer_uno(pedir_nombre())
    mostrar_tarjeta(datos) if datos else print("  ⚠  No encontrado.")


def flujo_actualizar(svc: ServicioEstudiantes) -> None:
    print("\n--- Actualizar Notas ---")
    nombre = pedir_nombre()
    actual = svc.leer_uno(nombre)
    if not actual:
        print("  ⚠  No encontrado.")
        return
    print(f"  Notas actuales: {actual['notas']}")
    notas_nuevas = pedir_notas()
    ok, msg = svc.actualizar(nombre, notas_nuevas)
    print(f"\n  {'✅' if ok else '⚠ '} {msg}")


def flujo_eliminar(svc: ServicioEstudiantes) -> None:
    print("\n--- Eliminar Estudiante ---")
    nombre = pedir_nombre()
    if not svc.existe(nombre):
        print("  ⚠  No encontrado.")
        return
    if not confirmar(f"¿Seguro que deseas eliminar a '{nombre}'?"):
        print("  Operación cancelada.")
        return
    ok, msg = svc.eliminar(nombre)
    print(f"\n  {'✅' if ok else '⚠ '} {msg}")
