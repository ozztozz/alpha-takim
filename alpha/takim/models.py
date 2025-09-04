from django.db import models
from django.urls import reverse
from PIL import Image
import uuid
from django.conf import settings
# Create your models here.
class Takim (models.Model):
    adi=models.CharField(max_length=50)
    renk=models.CharField(default='red', max_length=50)
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
    adi=models.CharField(max_length=50)
    soyadi=models.CharField(max_length=50)
    dogum_tarihi=models.DateField()
    okul=models.CharField(max_length=50)
    telefon=models.CharField(max_length=50, null=True,blank=True)
    veli=models.CharField(max_length=50)
    veli_telefon=models.CharField(max_length=50)
    veli_eposta=models.EmailField(max_length=50)
    takim=models.ForeignKey(Takim,on_delete=models.CASCADE ,null=True)
    aktif=models.BooleanField(default=True)
    created=models.DateTimeField(auto_now_add=True)
    s_uuid=models.UUIDField(default=uuid.uuid4, unique=True,
          primary_key=False, editable=False,null=True)

    kronik_hastalik=models.CharField(null=True,blank=True,max_length=50)
    kronik_hastalik.aciklama='Kronik hastalik var mi'
    sakatlik_ameliyat=models.CharField(null=True,blank=True ,max_length=50)
    kullanilan_ilac=models.CharField(null=True,blank=True ,max_length=50)
    alerji=models.CharField(null=True,blank=True ,max_length=50)
    kalp=models.CharField(null=True,blank=True ,max_length=50)
    sosyal=models.CharField(null=True,blank=True, max_length=50)
    kalabalik=models.CharField(null=True,blank=True ,max_length=50)
    dikkat=models.CharField(null=True,blank=True, max_length=50)
    komut=models.CharField(null=True,blank=True ,max_length=50)
    iliski=models.CharField(null=True,blank=True ,max_length=50)


    yuzme_gecmisi=models.CharField(null=True,blank=True ,max_length=50)
    yuzme_bilgisi=models.CharField(null=True,blank=True ,max_length=50)
    derinlik=models.TextField(choices=YES_NO,default='Hayır' ,max_length=50)
    su_korkusu=models.TextField(choices=YES_NO,default='Hayır' ,max_length=50)
    denizde_yuzme=models.TextField(choices=YES_NO,default='Evet' ,max_length=50)
    neden_yuzme=models.CharField(null=True,blank=True ,max_length=50)
    istek_yuzme=models.CharField(null=True,blank=True ,max_length=50)
    vade_yuzme=models.CharField(null=True,blank=True ,max_length=50)

    ulasim=models.CharField(null=True,blank=True ,max_length=50)
    katilim=models.CharField(null=True,blank=True ,max_length=50)
    diger_spor=models.CharField(null=True,blank=True ,max_length=50)
    aile_not=models.TextField(null=True,blank=True ,max_length=50)
    antrenor_not=models.TextField(null=True,blank=True ,max_length=50)

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


AYLAR= (
    (1, "Ocak"),
    (2, "Şubat"),
    (3, "Mart"),
    (4, "Nisan"),
    (5, "Mayıs"),
    (6, "Haziran"),
    (7, "Temmuz"),
    (8, "Ağustos"),
    (9, "Eylül"),
    (10, "Ekim"),
    (11, "Kasım"),
    (12, "Aralık"),

)

class Odeme(models.Model):
    sporcu=models.ForeignKey(Sporcu,on_delete=models.CASCADE)
    odeme_turu=models.CharField(choices=ODEME_TURU, max_length=50)
    malzeme_turu=models.CharField(choices=MALZEME_TURU,blank=True,null=True, max_length=50)
    yil=models.IntegerField()
    ay=models.IntegerField(choices=AYLAR)
    odendi=models.BooleanField(default=False)
    create_user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,)
    created=models.DateField(auto_now_add=True)
    updated=models.DateField(auto_now=True)


    class Meta:
        ordering = ["-yil","-ay"]

    def __str__(self):
        return self.sporcu.adi+'-'+str(self.created)+'-'+str(self.odeme_turu)+'-'+str(self.ay)