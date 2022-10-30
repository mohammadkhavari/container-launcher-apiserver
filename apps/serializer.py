from rest_framework import serializers
from apps.models import App, Run
import docker

class AppSerializer(serializers.ModelSerializer):
    class Meta:
        model = App
        fields = ["id", "created", "name", "image", "command", "envs"]
    
    def validate_envs(self, value):
        if isinstance(value, dict) and \
            all(isinstance(k, str) and (isinstance(v,
        str)) for k,v in value.items()):
            return value

        raise serializers.ValidationError("Value must be valid list of string key pairs")

class RunSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = Run
        fields = '__all__'  

    def get_status(self, obj):
        try:
            client = docker.from_env()
            container = client.containers.get(obj.containerId)
            return "Finished" if container.status == "exited" else "Running"
        except docker.errors.DockerException: # NotFound or APIError
            # if there's only two (Running, Finishied) states. Finished is more sensible here altough it may be destroyed without finishing its job.
            return "Finished"