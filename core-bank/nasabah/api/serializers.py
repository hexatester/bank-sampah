from rest_framework.serializers import ModelSerializer
from nasabah.models import Nasabah


class NasabahSerializer(ModelSerializer):
    class Meta:
        model = Nasabah
        exclude = ['user']
