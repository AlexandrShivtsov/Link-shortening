from django import forms

from link_shortening.models import Links


class LinksForm(forms.ModelForm):
    long_link = forms.URLField(widget=forms.URLInput(attrs={"class": "link_field", 
                                                            "id": "link",
                                                            "placeholder": "URL"}))
    
    time_to_delete = forms.IntegerField(min_value=1, max_value=365, widget=forms.TextInput(
                                                                    attrs={"class": "timt_to_delete_fild", 
                                                                           "id": "delete",
                                                                           "placeholder": "30"}))

    class Meta:
        model = Links
        fields = (
            'long_link',
            'time_to_delete',
        )
