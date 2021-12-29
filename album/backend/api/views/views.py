from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from ..permissions.permissions import IsOwnerOrReadOnly

from ..models.api_page import AlbumImage, Album
from ..serializers.serializers import AlbumSerializer, ImageSerializer
from rest_framework import generics, status
from user.models import User
from user.serializers import UserSerializer


class RegisterUserView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = True
            return Response(data, status.HTTP_200_OK)
        else:
            data = serializer.errors
            return Response(data)


class AlbumList(generics.ListCreateAPIView):
    queryset = Album.objects.annotate(num_items=Count('photos__pic'))
    serializer_class = AlbumSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [OrderingFilter]
    ordering_fields = ['created', 'num_items']

    def get_queryset(self):
        user = self.request.user
        return Album.objects.filter(owner=user)


class AlbumDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        return Album.objects.filter(owner=user)


class ImageList(generics.ListCreateAPIView):
    queryset = AlbumImage.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['created', 'album']
    filterset_fields = ['tags', 'album']

    def get_queryset(self):
        user = self.request.user
        return AlbumImage.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ImageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = AlbumImage.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        return AlbumImage.objects.filter(owner=user)
