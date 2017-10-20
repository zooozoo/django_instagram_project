from django import forms

__all__ = (
    'PostForm',
    'CommentForm'
)


class PostForm(forms.Form):
    photo = forms.ImageField()
    # text = forms.CharField(max_length=5)

class CommentForm(forms.Form):
    content = forms.CharField(
        widget=forms.Textarea,
    )

