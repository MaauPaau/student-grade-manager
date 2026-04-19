# student-grade-manager

Proyecto enfocado en demostrar fundamentos de ingeniería de software en Python: arquitectura por capas, desacoplamiento, lógica pura testeable y persistencia controlada.

---

## Funcionalidad

Permite registrar estudiantes y sus notas desde la terminal, calculando promedios automáticamente y determinando si cada estudiante aprueba o reprueba. Los datos se persisten en un archivo JSON local, por lo que sobreviven al cierre del programa.

Operaciones disponibles: **crear, leer, actualizar y eliminar** estudiantes (CRUD completo).

---

## Tecnologías

- **Python 3.10+** — sin dependencias externas, solo librería estándar
- **JSON** — persistencia local de datos
- **TypedDict** — tipado estricto entre capas
- **Arquitectura por capas** — separación clara de responsabilidades

---

## Arquitectura

```
UI  →  Service  →  Logic  →  Data
```

## Valor técnico

Este proyecto no es solo un CRUD. Está diseñado para demostrar:

- Separación de responsabilidades (arquitectura por capas)
- Desacoplamiento entre lógica, persistencia y presentación
- Código testeable mediante funciones puras
- Manejo de errores en persistencia
- Diseño escalable (facilita migración a base de datos o API)

## Escalabilidad

El diseño permite evolucionar fácilmente a:

- API REST (por ejemplo con Flask)
- Base de datos (reemplazando JSON)
- Interfaz web

Sin modificar la lógica principal.


| Capa | Archivo | Responsabilidad |
|---|---|---|
| Presentación | `ui.py` | `input()` y `print()` únicamente |
| Servicio | `service.py` | Orquesta lógica + persistencia |
| Lógica | `logic.py` | Funciones puras, CRUD sin efectos |
| Datos | `data.py` | Lee y escribe JSON |

Cada capa solo conoce a la siguiente. `ui.py` no importa `data.py` directamente; todo pasa por `service.py`. Si mañana se reemplaza JSON por una base de datos, solo cambian `data.py` y `service.py`.

---

## Estructura del proyecto

```
student-grade-manager/
├── main.py           # Punto de entrada
├── service.py        # Capa de servicio
├── logic.py          # Lógica pura y CRUD
├── data.py           # Persistencia JSON
├── ui.py             # Presentación e interacción
├── tests.py          # 24 tests unitarios
├── .gitignore
└── README.md
```

---

## Cómo ejecutar

```bash
# Clonar el repositorio
git clone https://github.com/MaauPaau/student-grade-manager.git
cd student-grade-manager

# Correr los tests primero
python tests.py

# Iniciar el programa
python main.py
```

No se requiere instalar ninguna dependencia.

---

## Tests

```bash
python tests.py
```

```
==================================================
  EJECUTANDO TESTS
==================================================
  ✅  test_calcular_promedio_basico
  ✅  test_calcular_promedio_un_elemento
  ✅  test_calcular_promedio_lista_vacia
  ... (24 tests en total)
==================================================
  Resultado: 24 pasados  |  0 fallados
==================================================
```

Los tests cubren:
- Lógica pura: `calcular_promedio`, `construir_resumen`, CRUD completo
- Capa de servicio: persistencia real en disco, recuperación ante archivos corruptos

---

## Ejemplo de uso

```
Bienvenido  —  0 estudiante(s) cargado(s).

══════════════════════════════════════
   SISTEMA DE GESTIÓN DE NOTAS  v4
══════════════════════════════════════
  1. Agregar estudiante       (Create)
  2. Ver todos los estudiantes (Read)
  3. Ver tabla de promedios    (Read)
  4. Buscar estudiante         (Read)
  5. Actualizar notas         (Update)
  6. Eliminar estudiante      (Delete)
  7. Salir
══════════════════════════════════════
  Opción (1-7): 3

--- Resumen de Promedios ---

  Nombre               Promedio  Estado
  ────────────────────────────────────────────
  Ana García              84.33  APROBADO ✅
  Luis Torres             47.50  REPROBADO ❌
```
