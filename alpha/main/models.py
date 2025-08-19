from django.db import models

from django.urls import reverse
from django.core.validators import RegexValidator
from django.conf import settings
from django.utils.text import slugify
# Create your models here.

ANTRONER_CHOICES = (
    ("BANT", "Baş Antrenor"),
    ("ANT","Antrenor"),
    ("DYT","Diyetisyen"),
    ( "PSK","Psikolog"),

)
BLOG_CHOICES = (
    ("BLOG", "Blog"),
    ("DUYURU","Duyuru"),
)

class Antrenor (models.Model):
    adi=models.CharField(max_length=30)
    soyadi=models.CharField(max_length=30)
    unvan=models.TextField(choices=ANTRONER_CHOICES,default='ANT')
    resim=models.ImageField(upload_to='media/')
    ozet=models.TextField()
    ozgecmis=models.TextField()
    telefon=models.CharField(max_length=10)
    instagram=models.CharField(max_length=50)
    aktif=models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.adi+' '+ self.soyadi
    def get_absolute_url(self):
        return reverse("antrenor_list", kwargs={"id": self.id})
    

class Branslar (models.Model):
    brans= models.CharField(max_length=50)
    ozet=models.TextField()
    aciklama=models.TextField()
    resim=models.ImageField(null=True,blank=True)
    aktif=models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.brans

    def get_absolute_url(self):
        return reverse("brans_detail", kwargs={"id": self.id})

class InstagramPost(models.Model):
    baslik=models.CharField(max_length=100, default='Fk Alpha Academy')
    link=models.TextField()
    created_date=models.DateTimeField(auto_now_add=True)
    aktif=models.BooleanField(default=True)

    def __str__(self):
        return self.baslik + '--'+str(self.created_date)

    class Meta:
        ordering = ["-created_date"]


class Blog (models.Model):
    tur=models.TextField(choices=BLOG_CHOICES,default='BLOG')
    baslik=models.CharField(max_length=100)
    metin=models.TextField()
    resim=models.ImageField(null=True,blank=True)
    slug=models.SlugField(unique=True)
    aktif=models.BooleanField(default=True)
    created_date=models.DateTimeField(auto_now_add=True)
    author=models.ForeignKey(Antrenor,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.baslik
    class Meta:
        ordering=["-created_date"]
    def get_absolute_url(self):
        return reverse("blog_detail", kwargs={"slug": self.slug})
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.baslik)
        super().save(*args, **kwargs)
    





KAYNAK_CHOICES = (
    ("INS", "Instagram"),
    ("INT","Internet"),
    ("TAV","Tavsiye"),
    ("DGR","Diğer"),
)
BEKLENTI_CHOICES = (
    ("OGR", "Yüzmeyi Öğrenmek"),
    ("TEK", "Stilli Yüzmek"),
    ("INT","Spor Yapmak"),
    ("TAV","Profosyonel Sporcu Olmak"),
    ("DGR","Diğer"),
)

DERS_CHOICES = (
    ("0", "Hiç Ders Almadı"),
    ("1", "Bir yıla kadar"),
    ("3","Bir yıl üç yıl"),
    ("4","Üç yıldan fazla"),
)
GRUP_CHOICES = (
    ("OZL", "Özel Ders"),
    ("GRP", "Grup Dersi"),
    ("TKM","Takım"),
)


class Basvuru (models.Model):
    adi=models.CharField(max_length=50)
    dogum_yili=models.IntegerField()
    boy=models.IntegerField()
    kilo=models.IntegerField()
    ayak=models.IntegerField()
    veli=models.CharField(max_length=50)
    phone_regex = RegexValidator(regex=r'^5.*$', message="Telefon numarası formatı: '+530 555 5555'")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True) # Validators should be a list
    kaynak=models.TextField(choices=KAYNAK_CHOICES)
    ders_suresi=models.TextField(choices=DERS_CHOICES)
    beklenti=models.TextField(choices=BEKLENTI_CHOICES)
    ders_turu=models.TextField(choices=GRUP_CHOICES)
    created_date=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return  self.adi
    def get_absolute_url(self):
        return reverse("basvuru_detail", kwargs={"id": self.pk})
    

