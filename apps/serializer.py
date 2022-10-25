from rest_framework import serializers
from apps.models import App
from docker.models.containers import Container

class AppSerializer(serializers.ModelSerializer):
    class Meta:
        model = App
        fields = ["id", "created", "name", "image", "command", "envs"]

class RunSerializer(serializers.Serializer):
    id = serializers.CharField()
    image = serializers.SerializerMethodField()
    name = serializers.CharField()
    status = serializers.CharField()

    def get_image(self, obj):
        return " ,".join(obj.image.tags)