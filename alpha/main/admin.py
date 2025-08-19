from django.contrib import admin
from .models import Branslar, Antrenor, InstagramPost,Blog,Basvuru

# Register your models here.
admin.site.register(Branslar)
admin.site.register(Basvuru)
admin.site.register(Antrenor)
admin.site.register(InstagramPost)
admin.site.register(Blog)
