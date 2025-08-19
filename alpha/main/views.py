from django.shortcuts import render,redirect,get_object_or_404
from .models import Branslar,Antrenor,InstagramPost,Blog,Basvuru
from .forms import BasvuruForm
from django.views.generic import CreateView,UpdateView


from django.shortcuts import get_object_or_404

def landing(request):
    brans_list=Branslar.objects.filter(aktif=True)
    instagram_list=InstagramPost.objects.filter(aktif=True)[:3]
    antrenor_list=Antrenor.objects.filter(aktif=True).order_by('soyadi')
    duyuru_list=Blog.objects.filter(tur='DUYURU',aktif=True)[:20]
    blog_list=Blog.objects.filter(tur='BLOG',aktif=True)[:6]
    return render(request, 'landing.html',{'brans_list':brans_list,
                                         'instagram_list':instagram_list,
                                         'antrenor_list':antrenor_list,
                                         'duyuru_list':duyuru_list,
                                         'blog_list':blog_list
                                         })
def index(request):
    brans_list=Branslar.objects.filter(aktif=True)
    instagram_list=InstagramPost.objects.filter(aktif=True)[:3]
    antrenor_list=Antrenor.objects.filter(aktif=True).order_by('soyadi')
    duyuru_list=Blog.objects.filter(tur='DUYURU',aktif=True)
    blog_list=Blog.objects.filter(tur='BLOG',aktif=True)[:4]
    return render(request, 'index.html',{'brans_list':brans_list,
                                         'instagram_list':instagram_list,
                                         'antrenor_list':antrenor_list,
                                         'duyuru_list':duyuru_list,
                                         'blog_list':blog_list
                                         })



# Create your views here

def iletisim(request):
    return render(request,'iletisim.html')

class Basvuru (CreateView):
    model= Basvuru
    form_class=BasvuruForm
    success_url = 'basvuru_basari'

def basvuru_basari(request):
    return render(request,'main/basvuru_basari.html')

def blog_detail (request,slug):
    blog= get_object_or_404(Blog,slug=slug)
    blog_list=Blog.objects.filter(tur='BLOG') [:10]
    return render(request,'blog_detail.html',{'blog':blog,
                                              'blog_list':blog_list})

def kvkk (request):
    return render(request,'kvkk.html')



