from ..models.api_page import Album,AlbumImage
from django.contrib import admin
#from garpix_page.admin import BasePageAdmin


'''@admin.register(ApiPage)
class ApiPageAdmin(BasePageAdmin):
    pass'''

admin.site.register(Album)
admin.site.register(AlbumImage)
