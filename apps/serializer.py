from rest_framework import serializers
from apps.models import App
from docker.models.containers import Container

class AppSerializer(serializers.ModelSerializer):
    class Meta:
        model = App
        fields = ["id", "created", "name", "image", "command", "envs"]

class RunSerializer(serializers.Serializer):
    launched_at = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    app_name = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    command = serializers.SerializerMethodField()
    envs = serializers.SerializerMethodField()
    id = serializers.CharField()

    def get_launched_at(self, obj):
        utc_str = obj.attrs["Created"]
        return utc_str

    def get_image(self, obj):
        return " ,".join(obj.image.tags)

    # As the task wants there are only two considered states
    def get_status(self, obj):
        return "Finished" if obj.status == "exited" else "Running"
    
    def get_command(self, obj):
        return obj.labels["applied_cmd"]
    
    def get_envs(self, obj):
        return eval(obj.labels["applied_envs"])

    def get_app_name(self, obj):
        return obj.labels["app_name"]