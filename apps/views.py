from apps.models import App, Run
from apps.serializer import AppSerializer, RunSerializer
from apps.utils import exceptions
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
import docker

class AppViewSet(viewsets.ModelViewSet):
    queryset = App.objects.all()
    serializer_class = AppSerializer

class RunList(APIView):
    """
    List all app's runs or run a new container from app
    """
    def get_docker_client(self):
        return docker.from_env()

    def get_app(self, pk):
        try: 
            return App.objects.get(pk=pk)
        except App.DoesNotExist:
            raise Http404

    def post(self, _, pk):
        app = self.get_app(pk)

        # label appId on container
        labels = {"appId":str(app.id)}
        
        try:
            client = self.get_docker_client()
            container = client.containers.run(image=app.image,
                                                command=app.command, 
                                                detach=True, 
                                                labels=labels, 
                                                environment=app.envs)
        except docker.errors.NotFound or docker.errors.ImageNotFound:
            raise exceptions.ImageNotFound
        except docker.errors.DockerException:
            raise exceptions.DockerAPIError

        data = {
                "created": container.attrs["Created"],
                "containerId": container.id,
                "app": app.id, 
                "app_name": app.name,
                "image": app.image,
                "command": app.command,
                "envs": app.envs,
                }

        serializer = RunSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def get(self, _, pk):
        # check app exists
        self.get_app(pk)
        queryset = Run.objects.filter(app=pk)
        serializer = RunSerializer(queryset, many=True)
        return Response(serializer.data)