from rest_framework import serializers
from user.models import User
from rest_framework.fields import ImageField
from ..models.api_page import AlbumImage, Album


class UserFilteredPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        request = self.context.get('request', None)
        queryset = super(UserFilteredPrimaryKeyRelatedField, self).get_queryset()
        if not request or not queryset:
            return None
        return queryset.filter(owner=request.user)


class ImageSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    thumb = ImageField(read_only=True)
    album = UserFilteredPrimaryKeyRelatedField(queryset=Album.objects)

    class Meta:
        model = AlbumImage
        fields = ['id', 'name', 'pic', 'thumb', 'owner', 'tags', 'created', 'album']

    def get_queryset(self):
        user = self.request.user
        return AlbumImage.objects.filter(owner=user)

    def create(self, validated_data):
        return AlbumImage.objects.create(**validated_data)


class AlbumSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    photos = ImageSerializer(many=True, read_only=True)
    photo_count = serializers.IntegerField(source='photos.count', read_only=True)
    created = serializers.ReadOnlyField()

    class Meta:
        model = Album
        fields = ['id',  'title', 'owner', 'description', 'created', 'photos', 'photo_count']
        depth = 1


class UserSerializer(serializers.ModelSerializer):
    album = AlbumSerializer(many=True, read_only=True)
    image = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'album', 'image']
