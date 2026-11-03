import json
import os

from modelos import Alumno, Documento, Solicitud

ARCHIVO_DATOS = "datos/datos.json"


class RepositorioSolicitudes:

    def __init__(self, archivo=ARCHIVO_DATOS):
        self.archivo = archivo

    def guardar(self, alumnos, solicitudes):
        datos = {"alumnos": [], "solicitudes": []}
        for alumno in alumnos:
            datos["alumnos"].append(
                {
                    "legajo": alumno.legajo,
                    "nombre": alumno.nombre,
                    "carrera": alumno.carrera,
                    "email": alumno.email,
                }
            )
        for solicitud in solicitudes:
            documentos = []
            for documento in solicitud.documentos:
                documentos.append(
                    {
                        "nombre": documento.nombre,
                        "tipo": documento.tipo,
                        "obligatorio": documento.obligatorio,
                    }
                )
            datos["solicitudes"].append(
                {
                    "id": solicitud.id,
                    "legajo": solicitud.legajo_alumno,
                    "tipo": solicitud.tipo,
                    "estado": solicitud.estado,
                    "fecha": solicitud.fecha_creacion,
                    "documentos": documentos,
                    "motivo": solicitud.motivo,
                }
            )
        carpeta = os.path.dirname(self.archivo)
        if carpeta:
            os.makedirs(carpeta, exist_ok=True)
        with open(self.archivo, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=2)

    def cargar(self):
        alumnos = []
        solicitudes = []
        if not os.path.exists(self.archivo):
            return alumnos, solicitudes
        with open(self.archivo, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
        for dato_alumno in datos["alumnos"]:
            alumnos.append(
                Alumno(
                    dato_alumno["legajo"],
                    dato_alumno["nombre"],
                    dato_alumno["carrera"],
                    dato_alumno["email"],
                )
            )
        for dato_solicitud in datos["solicitudes"]:
            solicitud = Solicitud(
                dato_solicitud["id"],
                dato_solicitud["legajo"],
                dato_solicitud["tipo"],
                dato_solicitud["estado"],
                dato_solicitud["fecha"],
            )
            solicitud.motivo = dato_solicitud.get("motivo")
            for dato_documento in dato_solicitud["documentos"]:
                solicitud.documentos.append(
                    Documento(
                        dato_documento["nombre"],
                        dato_documento["tipo"],
                        dato_documento["obligatorio"],
                    )
                )
            solicitudes.append(solicitud)
        return alumnos, solicitudes
