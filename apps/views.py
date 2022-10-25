from apps.models import App
from apps.serializer import AppSerializer, RunSerializer
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

class AppList(generics.ListCreateAPIView):
    queryset = App.objects.all()
    serializer_class = AppSerializer

class AppDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = App.objects.all()
    serializer_class = AppSerializer

class RunList(APIView):
    """
    List all app's runs or run a new container from app
    """
    def get_docker_client(self):
        import docker
        return docker.from_env()

    def get_app(self, pk):
        try: 
            return App.objects.get(pk=pk)
        except App.DoesNotExist:
            raise Http404

    def post(self, _, pk):
        app = self.get_app(pk)
        client = self.get_docker_client()
        serializer = AppSerializer(app)

        # label appId on container and 
        # specify applied environment variables, command, app name cause they may change
        labels = {"appId":str(app.id), "applied_envs":str(app.envs), "applied_cmd":app.command, "app_name": app.name}
        container = client.containers.run(image=app.image, command=app.command, detach=True, labels=labels, environment=serializer.data["envs"])
        serializer = RunSerializer(container)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def get(self, _, pk):
        # check app exists
        self.get_app(pk)
    
        client = self.get_docker_client()
        containers = client.containers.list(all=True, filters={"label":f'appId={pk}'})
        serializer = RunSerializer(containers, many=True)
        return Response(serializer.data)


