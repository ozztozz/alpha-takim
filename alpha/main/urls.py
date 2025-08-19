from django.urls import path
from .views import Basvuru, basvuru_basari,iletisim,blog_detail,landing,kvkk
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [    
   
    path('', landing, name='index'),
    path('basvuru/', Basvuru.as_view(), name='basvuru'),
    path('iletisim/', iletisim, name='iletisim'),
    path('basvuru/basvuru_basari/', basvuru_basari, name='basvuru_basari'),
    path('blog/<slug:slug>/', blog_detail, name='blog_detail'),
    path('kvkk/', kvkk, name='kvkk'),

  
] 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)