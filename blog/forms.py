from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    # type = forms.ChoiceField()
    # name = forms.CharField(max_length=20)
    # content = forms.Textarea()
    # email = forms.EmailField(required=False)

    class Meta:
        model = Contact
        fields = ( 'name', 'content', 'email')