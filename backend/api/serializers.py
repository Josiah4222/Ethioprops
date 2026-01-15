from rest_framework import serializers
from .models import Parcel
import json

class ParcelSerializer(serializers.ModelSerializer):
    geometry = serializers.SerializerMethodField()

    class Meta:
        model = Parcel
        fields = '__all__'

    def get_geometry(self, obj):
        try:
            return json.loads(obj.geometry_json)
        except:
            return None
