from rest_framework import viewsets, mixins, parsers, renderers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions

from api.serializers.user import UserSerializer
from api.models.user import User


class UserViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GetLoggedInUserViewSet(APIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user
        serialized = UserSerializer(user, context={"request":request})
        return Response(data=serialized.data, status=status.HTTP_200_OK)
