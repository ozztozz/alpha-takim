from django.shortcuts import render,get_object_or_404,redirect
from .models import Takim,Sporcu,Odeme,AYLAR
from .forms import FormSporcu,FormTakim,FormSaglik,FormYuzme,FormSporcuFull,FormUlasim,FormOdeme
from django.views.generic import CreateView,UpdateView,DeleteView
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.db.models.functions import ExtractYear
from datetime import date

# Create your views here.

@login_required(login_url='/')
def  dashboard(request):
    takimlar = Takim.objects.annotate(number_of_sporcu=Count('sporcu'))
    sporcular=Sporcu.objects.all().order_by('-id')[:10]
    form=FormTakim
    sporcuform=FormSporcu
    return render(request,'dashboard.html',{"takimlar":takimlar,'sporcular':sporcular,'form':form,'sporcuform':sporcuform})


@login_required(login_url='/')
def sporcu_list(request):
    takimlar = Takim.objects.annotate(number_of_sporcu=Count('sporcu'))
    sporcular=Sporcu.objects.all().order_by('-id')[:10]
    form=FormTakim
    sporcuform=FormSporcuFull


    return render(request,'sporcular.html',{"takimlar":takimlar,'sporcular':sporcular,'form':form,'sporcuform':sporcuform})

@login_required(login_url='/')
def takim_list(request):
    takimlar = Takim.objects.annotate(number_of_sporcu=Count('sporcu'))
    sporcular=Sporcu.objects.all().values('dogum_tarihi__year','takim__adi','takim__renk','adi','soyadi','takim__adi','s_uuid')
    takim_yas = sporcular.values('dogum_tarihi__year','takim__adi','takim__renk').annotate(sayi=Count('id'))
    print(sporcular)
   

    return render(request,'takimlar.html',{"takimlar":takimlar,'takim_yas':takim_yas,'sporcular':sporcular})

def modal(request):
    takimlar = Takim.objects.annotate(number_of_sporcu=Count('sporcu'))
    sporcular=Sporcu.objects.all().order_by('-id')[:4]
    return render(request,'modal.html',{"takimlar":takimlar,'sporcular':sporcular})


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


    response=render(request, 'sporcu_detay.html',{'sporcu':sporcu,
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

            return redirect('takim/')
    else:
        form=FormOdeme()
    return render(request,'odeme.html',{'form':form})
    