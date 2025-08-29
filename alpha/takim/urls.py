from django.urls import path
from .views import takim_list,CreateTakim,sporcu_ekle,updateSporcu,sporcudetay,sporcukayit,sporcu_list,dashboard,odeme_ekle

urlpatterns = [
    path('',dashboard,name='takim'),
    path('sporcular/',sporcu_list,name='sporcular'),
    path('takimlar/',takim_list,name='takim_list'),
    path('sporcukayit/',sporcukayit,name='sporcukayit'),
    path('sporcudetay/<uuid:s_uuid>/',sporcudetay,name='sporcudetay'),
    path('takimekle/',CreateTakim.as_view(),name='takimekle'),
    path('sporcuekle/',sporcu_ekle,name='sporcuekle'),
    path('sporcupdate/<uuid:s_uuid>/<str:detay>',updateSporcu,name='sporcupdate'),
    path('odeme/',odeme_ekle,name='odeme'),
    
]
