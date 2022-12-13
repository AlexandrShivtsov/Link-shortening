from django import forms

from link_shortening.models import Links


class LinksForm(forms.ModelForm):

    time_to_delete = forms.IntegerField(min_value=1, max_value=365, initial=90)

    class Meta:
        model = Links
        fields = (
            'long_link',
        )
