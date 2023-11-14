from rest_framework import serializers

from .models import PerevalAdded, StatusList, Authors, Coords


class CoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coords
        fields = '__all__'

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Authors
        fields = '__all__'

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusList
        fields = '__all__'

class PerevalSerializer_S(serializers.ModelSerializer):
    class Meta:
        model = PerevalAdded
        fields = '__all__'

class PerevalSerializer(serializers.ModelSerializer):
    coords = CoordsSerializer(read_only=True, many=False)
    users = UsersSerializer(read_only=True, many=False)
    obj_status = StatusSerializer(read_only=True, many=False)

    class Meta:
        model = PerevalAdded
        fields = '__all__'

class PerevalSerializerPost(serializers.ModelSerializer):
    coords = CoordsSerializer(read_only=True, many=False)
    users = UsersSerializer(read_only=False, many=False)
    obj_status = StatusSerializer(read_only=True, many=False)

    class Meta:
        model = PerevalAdded
        fields = '__all__'

class PerevalSerializerPatch(serializers.ModelSerializer):
    coords = CoordsSerializer(read_only=True, many=False)

    class Meta:
        model = PerevalAdded
        fields = '__all__'
