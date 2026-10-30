from rest_framework import serializers

from .models import Categoria, Moto, Repuesto


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = "__all__"


class MotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Moto
        fields = "__all__"


class RepuestoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repuesto
        fields = "__all__"