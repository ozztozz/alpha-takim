from django.shortcuts import render,get_object_or_404,redirect
from .models import Takim,Sporcu,Odeme,AYLAR,KISISEL_BILGILER
from .forms import FormSporcu,FormTakim,FormSaglik,FormYuzme,FormSporcuFull,FormUlasim,FormOdeme
from django.views.generic import CreateView,UpdateView,DeleteView
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.db.models.functions import ExtractYear
from datetime import date

# Create your views here.

@login_required
def  dashboard(request):
    bugun=date.today()
    ay=bugun.month-1
    yil=bugun.year
    
    if bugun.day>15:
        print(bugun.day)
        ay=ay+1
    takimlar = Takim.objects.filter(aktif=True).count()
    sporcular=Sporcu.objects.filter(aktif=True).count()
    odemeler=Odeme.objects.filter(ay=ay,yil=yil,odendi=True).count()
    form=FormTakim
    sporcuform=FormSporcu
    ay_adi=AYLAR[ay]
    return render(request,'dashboard.html',{'takimlar':takimlar,'sporcular':sporcular,'odemeler':odemeler,'ay_adi':ay_adi})


@login_required
def sporcu_list(request):
    takimlar = Takim.objects.annotate(number_of_sporcu=Count('sporcu'))
    sporcular=Sporcu.objects.all().order_by('-id')
    form=FormTakim
    sporcuform=FormSporcuFull


    return render(request,'sporcular.html',{"takimlar":takimlar,'sporcular':sporcular,'form':form,'sporcuform':sporcuform})

@login_required
def takim_list(request):
    takimlar = Takim.objects.annotate(number_of_sporcu=Count('sporcu'))
    sporcular=Sporcu.objects.all().values('dogum_tarihi__year','takim__adi','takim__renk','adi','soyadi','takim__adi','s_uuid')
    takim_yas = sporcular.values('dogum_tarihi__year','takim__adi','takim__renk').annotate(sayi=Count('id'))

   

    return render(request,'takimlar.html',{"takimlar":takimlar,'takim_yas':takim_yas,'sporcular':sporcular})

def modal(request):
    takimlar = Takim.objects.annotate(number_of_sporcu=Count('sporcu'))
    sporcular=Sporcu.objects.all().order_by('-id')[:4]
    return render(request,'modal.html',{"takimlar":takimlar,'sporcular':sporcular})


from django.core import serializers
def sporcubilgileri(request,s_uuid):
    sporcu=Sporcu.objects.filter(s_uuid=s_uuid).values().first()
    kisisel_bilgiler=[]
    index=0
    for kategori,data in KISISEL_BILGILER.items():
        kisisel_bilgiler.append({'kategori':kategori,'sorular':[]})
        for baslik,soru in data.items():
            kisisel_bilgiler[index]['sorular'].append({'baslik':baslik,'soru':soru,'bilgi':sporcu[baslik]})
        index=index+1
    return render(request, 'sporcu_bilgileri.html',{'sporcu':sporcu,'kisisel_bilgiler':kisisel_bilgiler})


def sporcudetay(request,s_uuid):
    bugun=date.today()
    sporcu=get_object_or_404(Sporcu,s_uuid=s_uuid)
    odemeler=Odeme.objects.filter(sporcu=sporcu,odeme_turu='Uyelik')
    odenmemis=False
    odeme_check=[]
    for ay in AYLAR:
        if ay[0]<=bugun.month:
            if odemeler.filter(ay=ay[0],odendi=True):
                odeme_check.append({'ay':ay[1],'odeme_tarihi':odemeler.filter(ay=ay[0]).first().updated})
            else:
                odeme_check.append({'ay':ay[1],'odeme_tarihi':None})
                odenmemis=True
    odeme_check.reverse()
    odeme_check=odeme_check[:3]
    
    
    if odemeler.filter(ay=bugun.month):
        odenmeyen=None
    else:
        odenmeyen=AYLAR[bugun.month][1] 

    formSaglik=FormSaglik(instance=sporcu)
    formYuzme=FormYuzme(instance=sporcu)
    formSporcu=FormSporcu(instance=sporcu)
    formUlasim=FormUlasim(instance=sporcu)

    
    kayit=True
    if request.COOKIES.get('s_uuid'):
        kayit=False


    response=render(request, 'sporcu_bilgileri.html',{'sporcu':sporcu,
                                                  'odenmemis':odenmemis,
                                                  'odeme_check':odeme_check,
                                                  'formSaglik':formSaglik,'formYuzme':formYuzme,
                                                  'formSporcu':formSporcu,'formUlasim':formUlasim,
                                                  'kayit':kayit})
    response.set_cookie('s_uuid',sporcu.s_uuid)
    
    return response

class CreateTakim(CreateView):
    model=Takim
    form_class=FormTakim
    
def sporcu_ekle(request):
   if request.method == "POST":
       form = FormSporcuFull(request.POST,request.FILES)
       if form.is_valid():
           sporcu=form.save()
           return redirect('/takim/sporcudetay/'+str(sporcu.s_uuid))  # Adjust this to your post list view
       
   else:
       form = FormSporcu()
   return render(request, 'partials/modal_sporcu.html', {'form': form})

def updateSporcu(request,s_uuid,detay=None):
    sporcu = get_object_or_404(Sporcu, s_uuid = s_uuid)

    if request.method == 'POST':
        post=request.POST
        post = request.POST.copy() # to make it mutable
        if request.FILES == None:
            post['resim'] = sporcu.resim        
        form=FormSporcu(post,request.FILES,instance=sporcu)
        if detay=='saglik':
            form=FormSaglik(post,request.FILES,instance=sporcu)    
        if detay=='yuzme':
            
            form=FormYuzme(post,request.FILES,instance=sporcu)
        if detay=='ulasim':
            form=FormUlasim(post,request.FILES,instance=sporcu)
        print(form.is_valid())
        if form.is_valid():
            print('aaa')
            form.save()
            return  redirect('/takim/sporcudetay/'+str(s_uuid))
    else:
        sporcuform=FormSporcu(instance = sporcu)

    return render(request,'partials/modal_sporcu.html',{'sporcuform':sporcuform,'sporcu':sporcu})

def sporcukayit(request):
    form=FormSporcuFull
    s_uuid=request.COOKIES.get('s_uuid')
    if s_uuid:
        return redirect('sporcudetay', s_uuid=s_uuid)
    else:
        return render(request,'sporcu_kayit.html',{'form':form})
    
def saglik_ekle(request):
   if request.method == "POST":
       form = FormSporcu(request.POST,request.FILES)
       print(form)
       if form.is_valid():
           sporcu=form.save()
           return redirect('/takim/sporcudetay/'+str(sporcu.s_uuid))  # Adjust this to your post list view
       
   else:
       form = FormSporcu()
   return render(request, 'takim/sporcu_form.html', {'form': form})




from django.views.decorators.cache import never_cache
@login_required
@never_cache
def odeme_ekle(request):
    if request.method=='POST':
        data=request.POST
        sporcu=data.get('sporcu')
        odeme_turu='Uyelik'
        yil=data.get('yil')
        ay=data.get('ay')
        if Odeme.objects.filter(sporcu=sporcu,odeme_turu=odeme_turu,yil=yil,ay=ay):
            odeme_var=Odeme.objects.get(sporcu=sporcu,odeme_turu=odeme_turu,yil=yil,ay=ay)
            form=FormOdeme(request.POST,instance=odeme_var)
        else:
            form=FormOdeme(request.POST)
        if form.is_valid():
            form.save()

            
    else:
        form=FormOdeme()
    return  redirect('/takim/odeme_list/'+ay)
    

@login_required
@never_cache
def odeme_list(request,ay=None):
    bugun=date.today()
    yil=bugun.year
    if ay==None:
        ay=bugun.month
    sporcular=Sporcu.objects.filter(aktif=True).values('adi','soyadi','takim__adi','id','resim').order_by('takim__adi','adi','soyadi',)
    odeyenler=[sporcu['sporcu'] for sporcu in Odeme.objects.filter(ay=ay,yil=yil,odendi=True).values('sporcu')]

    for sporcu in sporcular:
        form_bilgileri={'sporcu':sporcu['id'],"odeme_turu":'Uyelik',"yil":yil,"ay":ay,'create_user':1}
        if sporcu['id'] in odeyenler:           
            sporcu['odendi']=True
            form_bilgileri['odendi']=False
        else:
            sporcu['odendi']=False
            form_bilgileri['odendi']=True
        form=FormOdeme(initial=form_bilgileri)
        sporcu['form']=form
        sporcu['ay']=ay
        sporcu['ay_adi']=AYLAR[ay-1][1]
        sporcu['yil']=yil
    onceki_aylar=list(reversed(AYLAR[:bugun.month+1]))

    return render (request,'odeme_listesi.html',{'sporcular':sporcular,'aylar':onceki_aylar})

