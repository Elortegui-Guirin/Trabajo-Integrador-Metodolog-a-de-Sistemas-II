# Decisiones técnicas por etapa

Registro de las decisiones tomadas en cada etapa del TPI, con su justificación y el commit o tag
donde quedaron. El desarrollo completo está en el informe (`docs/Trabajo Integrador Metodologia II.html`).

## Etapa 1 — Sistema base (`estado-inicial`, `3b991c0`)

| Decisión | Justificación |
|----------|---------------|
| Dominio: Gestión de Solicitudes Académicas | Es el caso sugerido por la cátedra y permite reglas de negocio verificables (estados, documentos obligatorios) |
| Python 3, solo biblioteca estándar | Se ejecuta sin instalar nada y la evaluación se puede reproducir en cualquier máquina |
| Persistencia simulada con JSON | Cumple el requisito de persistencia sin depender de una base de datos |
| Aplicación de consola, sin autenticación | El foco del TPI está en la calidad interna, no en la interfaz |

## Etapas 2 y 3 — Diagnóstico (`etapa-diagnostico`, `292739c`)

| Decisión | Justificación |
|----------|---------------|
| Diagnosticar 10 code smells (el mínimo es 8) | Cubren duplicación, complejidad, distribución de responsabilidades y legibilidad |
| Priorizar por riesgo y costo de corrección | Primero los smells de riesgo alto que se corrigen con un refactoring acotado: Duplicated Code (1), God Class (2), Long Method (3) |
| Postergar Data Class y Complex Conditional | Tienen riesgo alto, pero corregirlos exige rediseñar el modelo de estados |

Los commits de las etapas 2, 3, 4, 5 y 7 no modifican archivos: marcan el momento en que se cerró cada
etapa del análisis, cuyo contenido está en el informe.

## Etapa 4 — SOLID y Clean Code

| Principio | Decisión |
|-----------|----------|
| SRP | Separar la persistencia del servicio (`RepositorioSolicitudes`) |
| OCP | Llevar los documentos por tipo a un diccionario (`RequisitosDocumentales.REQUISITOS`) |
| LSP | No aplica: no hay jerarquías de clases y no se agregan sin necesidad |
| ISP | No aplica en el estado inicial; el repositorio expone solo `guardar` y `cargar` |
| DIP | El servicio recibe el repositorio en el constructor, lo que permite reemplazarlo en las pruebas |

## Etapa 5 — Refactorings (`estado-refactorizado`, `bdb770f`)

| Refactoring | Commit | Smell que ataca |
|-------------|--------|-----------------|
| Extract Method: `buscar_solicitud()` | `0cac0ad` | #1 Duplicated Code |
| Move Method: `RepositorioSolicitudes` | `be18c02` | #3 God Class |
| Introduce Parameter Object: `RequisitosDocumentales` | `ad9c866` | #2 Long Method, OCP |
| Rename: constantes de estado y retorno | `bdb770f` | #4 Magic Number, #5 Primitive Obsession |

**Criterio de seguridad:** antes de cada commit se borró `datos/` y se comparó la salida de
`py src/main.py` con la del estado inicial.

## Etapa 6 — Pruebas (`etapa-pruebas`, `ae894b8`)

| Decisión | Justificación |
|----------|---------------|
| `unittest` de la biblioteca estándar | No agrega dependencias |
| `RepositorioEnMemoria` en las pruebas | Gracias a la inyección del repositorio, las pruebas no tocan el disco ni dependen de ejecuciones anteriores |
| Comparar la salida de la demostración como evidencia antes/después | La suite no se puede ejecutar sobre `estado-inicial`, porque ese código no permitía inyectar el repositorio |

Evidencia: `docs/evidencias/` (salidas idénticas antes y después; 15 pruebas en verde).

## Etapa 7 — Code review y correcciones

| Decisión | Commit | Justificación |
|----------|--------|---------------|
| Corregir "probante de pago" → "comprobante de pago" | `b41af34` | Ningún certificado podía aprobarse |
| Persistir el motivo de rechazo y declararlo en `Solicitud` | `c52b2f9` | Se perdía al recargar; reemplaza el uso de `hasattr` |
| Validar documentos también en `cambiar_estado()` | `194123d` | Era un camino para aprobar sin cumplir la regla de negocio |
| Nombres con intención, sin separadores, `with open` | `073ef39` | Completa lo planificado en la etapa 4 sin cambiar el comportamiento |
| Un commit por corrección, cada una con su prueba | — | Trazabilidad: cada cambio se puede revisar y revertir por separado |
| No corregir las transiciones `if/elif`, Data Class ni la validación duplicada | — | Exigen rediseño; quedan como deuda consciente con prioridad (ver `checklist-code-review.md`) |

Las tres correcciones de defectos cambian el comportamiento a propósito, así que no son refactorings.
Por eso se registran en la etapa 7 y no en la 5.
