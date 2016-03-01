# -*- coding: utf8 -*-
import floppyforms as forms
from django_apogee.models import Etape


class EnvoiEMailCenterViewForm(forms.Form):
    subject = forms.CharField(max_length=120)
    text = forms.CharField(widget=forms.Textarea(attrs={'cols': 80, 'rows': 20}))
    attachment = forms.FileField(required=False)
    etape = forms.ModelChoiceField(Etape.objects.by_centre_gestion('IED').order_by('lib_etp'))
    session = forms.ChoiceField(choices=(('1', 'Première session'), ('2', 'Seconde session')))
