from rest_framework import serializers

from .models import PerevalAdded

class CoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerevalAdded
        fields = '__all__'

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerevalAdded
        fields = '__all__'

class PerevalSerializer_S(serializers.ModelSerializer):
    class Meta:
        model = PerevalAdded
        fields = '__all__'

class PerevalSerializer(serializers.ModelSerializer):
    coords = CoordsSerializer(read_only=True, many=False)
    users = UsersSerializer(read_only=True, many=False)

    class Meta:
        model = PerevalAdded
        fields = '__all__'
