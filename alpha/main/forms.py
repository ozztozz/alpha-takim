from django import forms
from .models import Basvuru


class BransEkle(forms.Form):
    brans= forms.CharField(max_length=30)
    ozet=forms.TextInput()
    aciklama=forms.TextInput()
    aktif=forms.BooleanField()

class BasvuruForm(forms.ModelForm):
    class Meta:
        model=Basvuru
        fields="__all__"
        labels={'veli':'Adını Soyadınız ? (Veli)',
                'phone_number':'Telefon Numaranız ?',
                'adi':'Sporcunun Adı Soyadı ?',
                'kaynak':'Bizi nereden tanıyorsunuz ?',
                'ayak':'Ayakkabı numarası ?',
                'ders_suresi':'Daha önce yüzme dersi aldınız mı ?',
                'beklenti':'Yüzme sporunda hedefiniz nedir ?',
                'ders_turu':'Bizden ne tür bir hizmet bekliyorsunuz ?',
                }

    def __init__(self, *args, **kwargs):

        add_class="""class='bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500'>"""
        super(BasvuruForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = add_class
