# Code review — checklist técnico

**Proyecto:** Sistema de Gestión de Solicitudes Académicas
**Etapa:** 7 — Code review profesional
**Versión revisada:** tag `estado-refactorizado` (commit `bdb770f`)
**Revisión de las correcciones:** rama `main`, commits `b41af34`, `c52b2f9`, `194123d` y `073ef39`

## 1. Criterios de aceptación técnica

Un cambio se acepta cuando cumple **todos** estos criterios:

| # | Criterio | Cómo se verifica |
|---|----------|------------------|
| A1 | No altera el comportamiento externo esperado | La salida de `py src/main.py` es idéntica a la de `estado-inicial` (solo cambia la fecha del día) |
| A2 | Todas las pruebas automatizadas pasan | `py -m unittest discover -s tests -v` termina en `OK` |
| A3 | Cada defecto corregido tiene una prueba que lo cubre | La prueba falla sin la corrección y pasa con ella |
| A4 | El commit tiene un único propósito y un mensaje descriptivo | Revisión del historial (`git log --oneline`) |
| A5 | No quedan imports ni variables sin uso | Revisión del diff (verificado también con `pyflakes`) |
| A6 | Lo que no se corrige queda documentado con riesgo y prioridad | Sección 4 de este documento |

## 2. Checklist aplicado

**Estado en la revisión:** OK = cumple · REVISAR = cumple con observaciones · CORREGIR = no cumple.
**Estado final:** resultado después de aplicar las acciones correctivas.

| # | Criterio | Estado en la revisión | Observación | Acción correctiva | Commit | Estado final |
|---|----------|-----------------------|-------------|-------------------|--------|--------------|
| 1 | ¿Los nombres describen la intención? | REVISAR | Quedaban `puede`, `f`, `doc`, `obs` y variables de una letra (`a`, `s`, `d`) en `servicios.py` y `repositorio.py` | Renombrar a `transicion_valida`, `archivo`, `documento`, `condicion`, `alumno`, `solicitud` | `073ef39` | OK |
| 2 | ¿Hay código duplicado? | REVISAR | La búsqueda de solicitud se unificó (Extract Method), pero el chequeo "ya fue resuelta" sigue repetido en 3 métodos (smell #10). La corrección de `194123d` repite además la validación de documentos de `aprobar()` en `cambiar_estado()` | Ninguna en esta iteración: se documenta como deuda | — | Pendiente (D2) |
| 3 | ¿Cada método hace una sola cosa? | REVISAR | `aprobar()` todavía valida, decide, persiste e imprime | Ninguna en esta iteración | — | Pendiente (D3) |
| 4 | ¿Las reglas de negocio tienen una única fuente de verdad? | REVISAR | Los documentos por tipo están en `RequisitosDocumentales`, pero los tipos válidos se repiten en `crear_solicitud()` y las transiciones siguen en `cambiar_estado()` | Ninguna en esta iteración | — | Pendiente (D1) |
| 5 | ¿Se eliminaron los números y strings mágicos? | REVISAR | Estados y códigos de retorno están en `constantes.py`; los tipos de solicitud (`"EQUIVALENCIA"`, etc.) siguen como strings | Ninguna en esta iteración | — | Pendiente (D4) |
| 6 | ¿La persistencia está separada del negocio y guarda todos los datos? | CORREGIR | El motivo de rechazo no se guardaba en el JSON y se perdía al recargar. Además, `guardar()` creaba siempre la carpeta `datos/` aunque se usara otra ruta | Persistir `motivo` (compatible con JSON viejos) y crear la carpeta de la ruta configurada | `c52b2f9` | OK |
| 7 | ¿Las reglas de negocio se cumplen por todos los caminos? | CORREGIR | `cambiar_estado(id, "APROBADA")` permitía aprobar sin los documentos obligatorios, salteando la regla de `aprobar()` | Validar documentos obligatorios en `cambiar_estado()` antes de aprobar | `194123d` | OK |
| 8 | ¿Los datos de dominio son correctos? | CORREGIR | El requisito de CERTIFICADO decía `"probante de pago"`, así que ningún certificado podía aprobarse | Corregir a `"comprobante de pago"` | `b41af34` | OK |
| 9 | ¿Los recursos se liberan aunque haya errores? | REVISAR | Los archivos se abrían con `open()` y `close()` manual: ante una excepción quedaban abiertos | Usar `with open(...)` con `encoding="utf-8"` | `073ef39` | OK |
| 10 | ¿El código está libre de comentarios que reemplazan nombres? | REVISAR | 8 bloques separadores `# ---- NOMBRE ----` en `servicios.py` (uno con el typo "SOLICITDES") | Eliminarlos: los nombres de los métodos ya expresan la intención | `073ef39` | OK |
| 11 | ¿Las pruebas automatizadas existen y pasan? | OK | 11 pruebas en verde | Agregar una prueba por cada defecto corregido | `b41af34`, `c52b2f9`, `194123d` | OK (15/15) |
| 12 | ¿La persistencia tiene pruebas propias? | CORREGIR | `RepositorioSolicitudes` no estaba probado | Prueba de guardado y recarga en un directorio temporal (`TestPersistencia`) | `c52b2f9` | OK |
| 13 | ¿La matriz de transiciones se puede modificar sin riesgo? | CORREGIR | `cambiar_estado()` sigue con `if/elif` anidados (smell #8) | Ninguna en esta iteración | — | Pendiente (D1) |
| 14 | ¿Las entidades expresan su comportamiento? | CORREGIR | `modelos.py` sigue siendo Data Class (smell #6) | Ninguna en esta iteración | — | Pendiente (D5) |
| 15 | ¿Los identificadores son únicos? | REVISAR | El ID se calcula con `len(self.solicitudes) + 1`: si se eliminara una solicitud, se podría repetir | Ninguna en esta iteración (hoy no existe la operación de borrado) | — | Pendiente (D6) |
| 16 | ¿El README permite ejecutar y entender el proyecto? | CORREGIR | Mostraba una estructura que no existe (`docs/01-...md`, `prompts/`) y no explicaba cómo correr las pruebas | Actualizar estructura, instalación/uso, funcionalidades, tecnologías y pruebas | (este commit) | OK |

## 3. Feedback por corrección

**`b41af34` — Requisito de CERTIFICADO.**
Defecto funcional que no se veía en la demostración porque el certificado se rechazaba antes de intentar aprobarlo. Se agregó `test_aprobar_certificado_con_comprobante_de_pago`.

**`c52b2f9` — Persistencia del motivo de rechazo.**
Es el escenario que el smell #7 (Feature Envy) anticipaba: un atributo nuevo que nadie agregó a la serialización. Ahora `Solicitud` declara `motivo = None` desde el constructor, en lugar de crearlo dinámicamente y consultarlo con `hasattr`. La carga tolera archivos sin ese campo. Se agregó `TestPersistencia`, que cubre además el ítem 12.

**`194123d` — Aprobación sin documentos por `cambiar_estado`.**
Se cierra un camino alternativo que violaba la regla de negocio principal. Se agregaron dos pruebas: el cambio se rechaza sin documentos y se acepta con ellos. Como efecto secundario, la validación de documentos queda escrita en dos métodos. Se registra como deuda D2.

**`073ef39` — Clean Code.**
Es un cambio solo de estructura, sin cambio de comportamiento: las 15 pruebas pasan y la salida de la demostración es idéntica. `servicios.py` pasó de 227 a 209 líneas.

## 4. Deuda técnica pendiente (consciente)

| ID | Hallazgo | Riesgo | Prioridad | Propuesta |
|----|----------|--------|-----------|-----------|
| D1 | Transiciones en `if/elif` y tipos válidos repetidos fuera de `RequisitosDocumentales` | Alto si cambian las reglas | 1 | Diccionario `TRANSICIONES = {estado: [destinos]}` y validar el tipo contra `RequisitosDocumentales.REQUISITOS` |
| D2 | Validación "ya fue resuelta" ×3 y validación de documentos ×2 | Medio | 2 | Extract Method: `esta_resuelta(solicitud)` y `documentos_faltantes(solicitud)` |
| D3 | `aprobar()` mezcla validación, persistencia y salida por consola | Medio | 3 | Separar la presentación (los `print`) de la lógica del servicio |
| D4 | Tipos de solicitud como strings | Medio | 4 | Constantes o `Enum` para los tipos |
| D5 | Entidades sin comportamiento (Data Class) | Medio | 5 | Mover reglas a la entidad, por ejemplo `solicitud.esta_resuelta()` |
| D6 | ID calculado con `len() + 1` | Bajo con el alcance actual | 6 | Usar `max(id) + 1` o un contador persistido |

## 5. Cómo reproducir la revisión

```bash
py -m unittest discover -s tests -v          # 15 pruebas, todas OK
py src/main.py                               # comparar con la salida de estado-inicial
git log --oneline                            # trazabilidad de las correcciones
git show b41af34 c52b2f9 194123d 073ef39     # detalle de cada corrección
```
