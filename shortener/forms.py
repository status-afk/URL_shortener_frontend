from django import forms

class URLForm(forms.Form):
    original_url = forms.URLField(label="Enter original URL", max_length=200)
