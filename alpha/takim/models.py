from django.db import models
from django.urls import reverse
from PIL import Image
import uuid
from django.conf import settings
# Create your models here.
class Takim (models.Model):
    adi=models.CharField()
    renk=models.CharField(default='red')
    aktif=models.BooleanField(default=True)
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.adi



YES_NO= (
    ("Evet", "Evet"),
    ("Hayır","Hayır"),

)

unvan=models.TextField(choices=YES_NO,default='Hayır')
class Sporcu(models.Model):
    resim=models.ImageField(null=True,blank=True,upload_to='media/')
    adi=models.CharField()
    soyadi=models.CharField()
    dogum_tarihi=models.DateField()
    okul=models.CharField()
    telefon=models.CharField(null=True,blank=True)
    veli=models.CharField()
    veli_telefon=models.CharField()
    veli_eposta=models.EmailField()
    takim=models.ForeignKey(Takim,on_delete=models.CASCADE ,null=True)
    aktif=models.BooleanField(default=True)
    created=models.DateTimeField(auto_now_add=True)
    s_uuid=models.UUIDField(default=uuid.uuid4, unique=True,
          primary_key=False, editable=False,null=True)

    kronik_hastalik=models.CharField(null=True,blank=True)
    sakatlik_ameliyat=models.CharField(null=True,blank=True)
    kullanilan_ilac=models.CharField(null=True,blank=True)
    alerji=models.CharField(null=True,blank=True)
    kalp=models.CharField(null=True,blank=True)
    sosyal=models.CharField(null=True,blank=True)
    kalabalik=models.CharField(null=True,blank=True)
    dikkat=models.CharField(null=True,blank=True)
    komut=models.CharField(null=True,blank=True)
    iliski=models.CharField(null=True,blank=True)


    yuzme_gecmisi=models.CharField(null=True,blank=True)
    yuzme_bilgisi=models.CharField(null=True,blank=True)
    derinlik=models.TextField(choices=YES_NO,default='Hayır')
    su_korkusu=models.TextField(choices=YES_NO,default='Hayır')
    denizde_yuzme=models.TextField(choices=YES_NO,default='Evet')
    neden_yuzme=models.CharField(null=True,blank=True)
    istek_yuzme=models.CharField(null=True,blank=True)
    vade_yuzme=models.CharField(null=True,blank=True)

    ulasim=models.CharField(null=True,blank=True)
    katilim=models.CharField(null=True,blank=True)
    diger_spor=models.CharField(null=True,blank=True)
    aile_not=models.TextField(null=True,blank=True)
    antrenor_not=models.TextField(null=True,blank=True)

    def get_absolute_url(self):
        return reverse("sporcudetay", kwargs={"s_uuid": self.s_uuid})

    def __str__(self):
        return self.adi+' '+ self.soyadi

    def get_dogum_yili(self):
        return self.dogum_tarihi.year

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Resize profile image to 150x150
        if self.resim:
            img = Image.open(self.resim.path)
            width, height = img.size
            
            bolen=4
            if width>3000:
                bolen=10
            if width>1000:
                img = img.resize((img.width // bolen, img.height // bolen))
                img.save(self.resim.path)


ODEME_TURU= (
    ("Uyelik", "Uyelik"),
    ("MALZEME", "Malzeme"),
)
MALZEME_TURU= (
    ("T-shirt", "T-shirt"),
    ("Esofman", "Esofman"),
    ("Bone", "Bone"),
    ("Bere", "Bere"),
    ("Corap", "Corap"),
)

class Odeme(models.Model):
    sporcu=models.ForeignKey(Sporcu,on_delete=models.CASCADE)
    odeme_turu=models.CharField(choices=ODEME_TURU)
    malzeme_turu=models.CharField(choices=MALZEME_TURU,blank=True,null=True)
    yil=models.IntegerField()
    ay=models.IntegerField()
    created=models.DateField(auto_created=True)
    updated=models.DateField(auto_now_add=True)
    create_user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,)

    def __str__(self):
        return self.sporcu.adi+'-'+str(self.created)+'-'+str(self.odeme_turu)