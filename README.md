# TPI — Metodología de Sistemas II

**Trabajo Práctico Integrador:** diagnóstico, refactorización y revisión técnica de un
sistema de Gestión de Solicitudes Académicas.

- **Autoras:** Rosario Iturralde y Veronica Guirin
- **Materia:** Metodología de Sistemas II
- **Carrera:** Tecnicatura Universitaria en Programación (UTN) — modalidad a distancia

## Descripción

Aplicación de consola que permite a los alumnos de una institución gestionar solicitudes
administrativas: equivalencias, certificados y reclamos. Cada solicitud recorre un ciclo de vida
y, para aprobarse, debe tener adjuntos los documentos obligatorios de su tipo.

```
PENDIENTE → EN_REVISION → APROBADA / RECHAZADA
```

| Tipo de solicitud | Documentos obligatorios |
|-------------------|-------------------------|
| EQUIVALENCIA | Plan de estudio, Syllabus |
| CERTIFICADO | Comprobante de pago |
| RECLAMO | — |

## Funcionalidades

- Alta de alumnos.
- Creación de solicitudes, validando el legajo y el tipo.
- Adjuntar documentos (solo a solicitudes no resueltas).
- Cambio de estado con validación de transiciones y de documentos obligatorios.
- Aprobación y rechazo con motivo.
- Listado de solicitudes por alumno y detalle de una solicitud.
- Persistencia de los datos en un archivo JSON (`datos/datos.json`).

## Tecnologías

- Python 3.8 o superior, solo biblioteca estándar (sin dependencias externas).
- `unittest` para las pruebas automatizadas.
- Git y GitHub para el control de versiones, con tags por etapa.

## Instalación y uso

```bash
git clone https://github.com/Elortegui-Guirin/Trabajo-Integrador-Metodolog-a-de-Sistemas-II.git
cd Trabajo-Integrador-Metodolog-a-de-Sistemas-II

# Demostración: da de alta un alumno, crea dos solicitudes, adjunta documentos,
# aprueba una y rechaza la otra.
py src/main.py

# Pruebas automatizadas
py -m unittest discover -s tests -v
```

En Linux o macOS, usar `python3` en lugar de `py`. Para repetir la demostración desde cero, hay que
borrar antes la carpeta `datos/`.

## Estructura del repositorio

```
├── README.md
├── docs/
│   ├── Trabajo Integrador Metodologia II.html   ← informe
│   ├── checklist-code-review.md   ← checklist técnico, correcciones y deuda pendiente (etapa 7)
│   ├── decisiones-tecnicas.md     ← decisiones por etapa y su justificación
│   └── evidencias/                ← salidas antes/después de la demostración y de las pruebas
├── src/
│   ├── main.py           ← demostración por consola
│   ├── modelos.py        ← entidades: Alumno, Solicitud, Documento
│   ├── servicios.py      ← reglas de negocio (ServicioSolicitudes)
│   ├── repositorio.py    ← persistencia JSON (RepositorioSolicitudes)
│   ├── requisitos.py     ← documentos obligatorios por tipo (RequisitosDocumentales)
│   └── constantes.py     ← estados y códigos de retorno
└── tests/
    └── test_solicitudes.py   ← 15 pruebas automatizadas
```

## Etapas y tags del TPI

| Tag | Etapa |
|-----|-------|
| `estado-inicial` | Sistema base seleccionado y descrito (etapa 1) |
| `etapa-diagnostico` | Deuda técnica y code smells (etapa 3) |
| `estado-refactorizado` | Código con los 4 refactorings aplicados (etapa 5) |
| `etapa-refactoring` | Documentación de los refactorings (etapa 5) |
| `etapa-pruebas` | Suite de pruebas y verificación antes/después (etapa 6) |
| `etapa-docs` | Code review con checklist (etapa 7) |

Para comparar las versiones:

```bash
git diff estado-inicial estado-refactorizado --stat
```

## Refactorings aplicados

1. **Extract Method:** `buscar_solicitud()` reemplaza un bloque repetido en 5 métodos.
2. **Move Method:** la persistencia pasa a `RepositorioSolicitudes`, que se inyecta en el servicio.
3. **Introduce Parameter Object:** `RequisitosDocumentales` centraliza los documentos por tipo.
4. **Rename:** constantes para estados y códigos de retorno.

A partir del code review se corrigieron, además, tres defectos y aspectos de Clean Code. El
detalle está en [`docs/checklist-code-review.md`](docs/checklist-code-review.md).

## Uso de inteligencia artificial

Este trabajo usó herramientas de IA como apoyo, según lo permitido por la cátedra. La
herramienta, la finalidad, el grado de intervención y el registro de prompts se declaran en el
informe. La autoría de las decisiones y del contenido entregado es de las integrantes.
