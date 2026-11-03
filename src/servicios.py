from datetime import datetime

from modelos import Alumno, Documento, Solicitud
from repositorio import RepositorioSolicitudes
from requisitos import RequisitosDocumentales
from constantes import (
    ESTADO_PENDIENTE,
    ESTADO_EN_REVISION,
    ESTADO_APROBADA,
    ESTADO_RECHAZADA,
    RESULTADO_NO_ENCONTRADA,
    RESULTADO_YA_RESUELTA,
    RESULTADO_FALTAN_DOCUMENTOS,
    RESULTADO_EXITO,
)


class ServicioSolicitudes:

    def __init__(self, repositorio=None):
        self.alumnos = []
        self.solicitudes = []
        if repositorio is None:
            repositorio = RepositorioSolicitudes()
        self.repositorio = repositorio
        self.alumnos, self.solicitudes = self.repositorio.cargar()

    def buscar_solicitud(self, id_solicitud):
        for solicitud in self.solicitudes:
            if solicitud.id == id_solicitud:
                return solicitud
        return None

    def guardar(self):
        self.repositorio.guardar(self.alumnos, self.solicitudes)

    def alta_alumno(self, legajo, nombre, carrera, email):
        alumno = Alumno(legajo, nombre, carrera, email)
        self.alumnos.append(alumno)
        self.guardar()
        print("Alumno dado de alta: " + nombre + " (legajo " + str(legajo) + ")")
        return alumno

    def crear_solicitud(self, legajo, tipo):
        alumno_encontrado = None
        for alumno in self.alumnos:
            if alumno.legajo == legajo:
                alumno_encontrado = alumno
        if alumno_encontrado is None:
            print("Error: el legajo " + str(legajo) + " no existe")
            return None

        if tipo != "EQUIVALENCIA" and tipo != "CERTIFICADO" and tipo != "RECLAMO":
            print("Error: tipo de solicitud invalido")
            return None

        nuevo_id = len(self.solicitudes) + 1
        solicitud = Solicitud(
            nuevo_id,
            legajo,
            tipo,
            ESTADO_PENDIENTE,
            datetime.now().strftime("%d/%m/%Y"),
        )
        self.solicitudes.append(solicitud)
        self.guardar()
        print(
            "Solicitud "
            + str(nuevo_id)
            + " creada para "
            + alumno_encontrado.nombre
            + " el "
            + solicitud.fecha_creacion
        )
        return solicitud

    def adjuntar_documento(self, id_solicitud, nombre, tipo, obligatorio):
        solicitud = self.buscar_solicitud(id_solicitud)
        if solicitud is None:
            print("Error: la solicitud " + str(id_solicitud) + " no existe")
            return None
        if solicitud.estado == ESTADO_APROBADA or solicitud.estado == ESTADO_RECHAZADA:
            print("Error: la solicitud ya fue resuelta, no se pueden adjuntar documentos")
            return None
        documento = Documento(nombre, tipo, obligatorio)
        solicitud.documentos.append(documento)
        self.guardar()
        print("Documento '" + nombre + "' adjuntado a la solicitud " + str(id_solicitud))
        return documento

    def cambiar_estado(self, id_solicitud, nuevo_estado):
        solicitud = self.buscar_solicitud(id_solicitud)
        if solicitud is None:
            print("Error: la solicitud " + str(id_solicitud) + " no existe")
            return False

        transicion_valida = False
        if solicitud.estado == ESTADO_PENDIENTE and nuevo_estado == ESTADO_EN_REVISION:
            transicion_valida = True
        elif solicitud.estado == ESTADO_EN_REVISION and (
            nuevo_estado == ESTADO_APROBADA or nuevo_estado == ESTADO_RECHAZADA
        ):
            transicion_valida = True
        elif solicitud.estado == ESTADO_PENDIENTE and (
            nuevo_estado == ESTADO_APROBADA or nuevo_estado == ESTADO_RECHAZADA
        ):
            transicion_valida = True

        if not transicion_valida:
            print(
                "Transicion invalida: "
                + solicitud.estado
                + " -> "
                + nuevo_estado
            )
            return False

        if nuevo_estado == ESTADO_APROBADA:
            faltantes = RequisitosDocumentales(solicitud.tipo).faltantes(solicitud.documentos)
            if len(faltantes) > 0:
                print("No se puede aprobar. Faltan documentos: " + str(faltantes))
                return False

        solicitud.estado = nuevo_estado
        self.guardar()
        print("Solicitud " + str(id_solicitud) + " ahora esta en estado " + nuevo_estado)
        return True

    def aprobar(self, id_solicitud):
        solicitud = self.buscar_solicitud(id_solicitud)
        if solicitud is None:
            print("Error: solicitud " + str(id_solicitud) + " no encontrada")
            return RESULTADO_NO_ENCONTRADA
        if solicitud.estado == ESTADO_APROBADA or solicitud.estado == ESTADO_RECHAZADA:
            print("Error: la solicitud ya fue resuelta")
            return RESULTADO_YA_RESUELTA

        requisitos = RequisitosDocumentales(solicitud.tipo)
        faltantes = requisitos.faltantes(solicitud.documentos)

        if len(faltantes) > 0:
            print("No se puede aprobar. Faltan documentos: " + str(faltantes))
            solicitud.estado = ESTADO_EN_REVISION
            self.guardar()
            return RESULTADO_FALTAN_DOCUMENTOS

        solicitud.estado = ESTADO_APROBADA
        self.guardar()
        print("Solicitud " + str(id_solicitud) + " APROBADA con exito")
        return RESULTADO_EXITO

    def rechazar(self, id_solicitud, motivo):
        solicitud = self.buscar_solicitud(id_solicitud)
        if solicitud is None:
            print("Error: solicitud " + str(id_solicitud) + " no encontrada")
            return RESULTADO_NO_ENCONTRADA
        if solicitud.estado == ESTADO_APROBADA or solicitud.estado == ESTADO_RECHAZADA:
            print("Error: la solicitud ya fue resuelta")
            return RESULTADO_YA_RESUELTA

        solicitud.estado = ESTADO_RECHAZADA
        solicitud.motivo = motivo
        self.guardar()
        print("Solicitud " + str(id_solicitud) + " RECHAZADA. Motivo: " + motivo)
        return RESULTADO_EXITO

    def listar_solicitudes_de_alumno(self, legajo):
        resultado = []
        for solicitud in self.solicitudes:
            if solicitud.legajo_alumno == legajo:
                resultado.append(solicitud)
        if len(resultado) == 0:
            print("El legajo " + str(legajo) + " no tiene solicitudes")
        else:
            print("Solicitudes del legajo " + str(legajo) + ":")
            for solicitud in resultado:
                print(
                    "  #"
                    + str(solicitud.id)
                    + " "
                    + solicitud.tipo
                    + " "
                    + solicitud.estado
                    + " ("
                    + str(len(solicitud.documentos))
                    + " documentos)"
                )
        return resultado

    def ver_detalle(self, id_solicitud):
        solicitud = self.buscar_solicitud(id_solicitud)
        if solicitud is None:
            print("Error: la solicitud " + str(id_solicitud) + " no existe")
            return None
        print("Detalle de la solicitud #" + str(solicitud.id))
        print("  Tipo: " + solicitud.tipo)
        print("  Estado: " + solicitud.estado)
        print("  Fecha: " + solicitud.fecha_creacion)
        print("  Legajo del alumno: " + str(solicitud.legajo_alumno))
        print("  Documentos:")
        for documento in solicitud.documentos:
            if documento.obligatorio:
                condicion = "obligatorio"
            else:
                condicion = "opcional"
            print("    - " + documento.nombre + " (" + documento.tipo + ", " + condicion + ")")
        if solicitud.motivo:
            print("  Motivo de rechazo: " + solicitud.motivo)
        return solicitud
