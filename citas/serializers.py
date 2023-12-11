from authentication.serializers import UsuarioSerializer
from rest_framework import serializers

from .models import Cita, Especialista, Invitado, Servicio


class ServicioSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Servicio
        fields = ("id", "nombre", "descripcion")


class EspecialistaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Especialista
        fields = ("id", "nombre", "especialidades")


class InvitadoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Invitado
        fields = ("nombre", "email")


class CitaSerializer(serializers.HyperlinkedModelSerializer):
    usuario = UsuarioSerializer(many=False)
    invitado = InvitadoSerializer(many=False)
    servicio = ServicioSerializer(many=False)
    especialista = EspecialistaSerializer(many=False)

    class Meta:
        model = Cita
        fields = ("id", "usuario", "invitado", "servicio", "especialista", "fecha")
