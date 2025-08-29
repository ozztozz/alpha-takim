from django import forms
from.models import Takim,Sporcu,Odeme

class FormTakim(forms.ModelForm):
    class Meta:
        model=Takim
        fields='__all__'
    def __init__(self, *args, **kwargs):

        add_class='w-full px-5 py-1 text-gray-700 bg-gray-200 rounded'
        super(FormTakim, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = add_class

class FormSporcu(forms.ModelForm):
    class Meta:
        model=Sporcu

        fields = ('resim','adi','soyadi','dogum_tarihi','okul','telefon','veli','veli_telefon','veli_eposta','takim')
        widgets = {
      'dogum_tarihi': forms.DateInput(attrs={ 'type': 'date',})
   }
    def __init__(self, *args, **kwargs):

        add_class='w-full px-5 py-1 text-gray-700 bg-gray-200 rounded'
        super(FormSporcu, self).__init__(*args, **kwargs)
        self.fields['takim'].required = False
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = add_class
        



class FormSaglik(forms.ModelForm):
    class Meta:
        model=Sporcu
        fields = ('kronik_hastalik','sakatlik_ameliyat','kullanilan_ilac','alerji','kalp','sosyal','kalabalik','komut')
    def __init__(self, *args, **kwargs):

        add_class='w-full px-5 py-1 text-gray-700 bg-gray-200 rounded'
        super(FormSaglik, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = add_class

BRANS_CHOICES = {
    "Serbest": "Serbest",
    "Sırtüstü": "Sırtüstü",
    "Kelebek": "Kelebek",
    "Kurbağalama": "Kurbağalama",
}

class FormYuzme(forms.ModelForm):
   
    class Meta:
        model=Sporcu
        fields = ('yuzme_gecmisi','yuzme_bilgisi','derinlik','su_korkusu','denizde_yuzme','neden_yuzme','istek_yuzme','vade_yuzme','diger_spor')
      
    def __init__(self, *args, **kwargs):

        add_class='w-full px-5 py-1 text-gray-700 bg-gray-200 rounded'
        super(FormYuzme, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = add_class

class FormUlasim(forms.ModelForm):
    class Meta:
        model=Sporcu
        fields = ('aile_not','antrenor_not')
    def __init__(self, *args, **kwargs):

        add_class='w-full px-5 py-1 text-gray-700 bg-gray-200 rounded'
        super(FormUlasim, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = add_class


class FormSporcuFull(forms.ModelForm):
    class Meta:
        model=Sporcu

        fields=('resim','adi','soyadi','dogum_tarihi','okul','telefon','veli','veli_telefon','veli_eposta','takim',
                'kronik_hastalik','sakatlik_ameliyat','kullanilan_ilac','alerji','kalp','sosyal','kalabalik','komut',
                'yuzme_gecmisi','yuzme_bilgisi','derinlik','su_korkusu','denizde_yuzme','neden_yuzme','istek_yuzme','vade_yuzme',
                'diger_spor','aile_not','antrenor_not'
                )
        widgets = {
      'dogum_tarihi': forms.DateInput(attrs={ 'type': 'date',}),
      'telefon': forms.TextInput(attrs={ 'type': 'tel',}),

   }
    def __init__(self, *args, **kwargs):

        add_class='w-full px-5 py-1 text-gray-700 bg-gray-200 rounded'
        super(FormSporcuFull, self).__init__(*args, **kwargs)
        self.fields['takim'].required = False
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = add_class

class FormOdeme(forms.ModelForm):
    class Meta:
        model=Odeme
        fields='__all__'

    def __init__(self, *args, **kwargs):

        add_class='w-full px-5 py-1 text-gray-700 bg-gray-200 rounded'
        super(FormOdeme, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = add_class