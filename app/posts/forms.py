from django import forms

from .models import Post


class PostForm(forms.Form):
    photo = forms.ImageField(
        label='사진',
        widget=forms.FileInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    content = forms.CharField(
        label='내용',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    def save(self, author):
        return Post.objects.create(
            author=author,
            photo=self.cleaned_data['photo'],
            content=self.cleaned_data['content'],
        )
