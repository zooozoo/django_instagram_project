from django import forms

__all__ = (
    'PostForm',
)


class PostForm(forms.Form):
    photo = forms.ImageField()
    text = forms.CharField(max_length=5)

    # def clean_text(self):
    #     data = self.cleaned_data['text']
    #     if data !=