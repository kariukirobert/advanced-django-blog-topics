from django import forms
from .models import Post


class PostForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Post Title', 'class': 'form-control'
        }))
    slug = forms.SlugField(widget=forms.TextInput(attrs={
        'placeholder': 'Post-Title-Slug', 'class': 'form-control'
    }))
    # image = forms.FileField()
    content = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Post Content', 'class': 'form-control'
    }))
    publish_date = forms.DateField(widget=forms.DateInput(attrs={
        'type':'date', 'class': 'form-control'
    }))


class PostModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'image', 'content', 'publish_date']
    

    def clean_title(self, *args, **kwargs):
        instance = self.instance
        title = self.cleaned_data.get('title')
        qs = Post.objects.filter(title__iexact=title)
        if instance is not None:
            qs = qs.exclude(pk=instance.pk)
        if qs.exists():
            raise forms.ValidationError("This title is already in use")
            
        return title