from modeltranslation.translator import TranslationOptions, register
from ..models import ApiPage


@register(ApiPage)
class ApiPageTranslationOptions(TranslationOptions):
    pass
