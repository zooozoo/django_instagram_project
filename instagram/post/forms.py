from django import forms

from .models import Post, PostComment

__all__ = (
    'PostForm',
    'CommentForm'
)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            'photo',
        )

    def save(self, commit=True, *args, **kwargs):
        if not self.instance.pk and commit:
            author = kwargs.pop('author', None)
            if not author:
                raise ValueError('Author field is required')
            self.instance.author = author
        return super().save(*args, **kwargs)


class CommentForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = (
            'content',
        )
        widget = {
            'content': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            )
        }