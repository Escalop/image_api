from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
import rest_framework.filters
from rest_framework.response import Response

from ..models.api_page import AlbumImage, Album
from ..serializers.serializers import AlbumSerializer, ImageSerializer
from rest_framework import generics, status, filters
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


class UserFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(owner=request.user)


class AlbumList(generics.ListCreateAPIView):
    queryset = Album.objects.annotate(num_items=Count('photos__pic'))
    serializer_class = AlbumSerializer
    filter_backends = [rest_framework.filters.OrderingFilter, UserFilterBackend]
    ordering_fields = ['created', 'num_items']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class AlbumDetail(generics.RetrieveUpdateDestroyAPIView):

    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

    def get_queryset(self):
        user = self.request.user
        return Album.objects.filter(owner=user)


class ImageList(generics.ListCreateAPIView):
    queryset = AlbumImage.objects.all()
    serializer_class = ImageSerializer
    filter_backends = [rest_framework.filters.OrderingFilter, DjangoFilterBackend, UserFilterBackend]
    ordering_fields = ['created', 'album']
    filterset_fields = ['tags', 'album']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return AlbumImage.objects.filter(owner=user)


class ImageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = AlbumImage.objects.all()
    serializer_class = ImageSerializer

    def get_queryset(self):
        user = self.request.user
        return AlbumImage.objects.filter(owner=user)
