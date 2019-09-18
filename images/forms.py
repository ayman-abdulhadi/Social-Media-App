from django import forms
from .models import Image, Comment
from urllib import request
from django.core.files.base import ContentFile
from django.utils.text import slugify


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model   = Image
        fields  = ('title', 'body', 'image', 'url')
        widgets = {
            'image' : forms.FileInput(attrs={'name':'image', 'class':'custom-file-input', 'id':'customFile'}),
            'url'   : forms.URLInput(attrs={'name':'url','class':'form-control' ,'placeholder':'Post Image URL'}),
            'body'  : forms.Textarea(attrs={'name':'desc',"class":"form-control", "id":"message", "rows":"3", "placeholder":"What are you thinking?"}),
            'title' : forms.TextInput(attrs={'name':'desc',"class":"form-control", "id":"message", "rows":"1", "placeholder":"Image Title (required)"}),
        }

    def clean(self):
        cd = self.cleaned_data
        if not cd['image'] and not cd['url']:
            raise forms.ValidationError('Please upload an image or give image url.')
        return cd

    def clean_url(self):
        url = self.cleaned_data['url']
        if url:
            valid_extensions = ['jpg', 'jpeg']
            extension        = url.rsplit('.',1)[1].lower()
            if extension not in valid_extensions:
                raise forms.ValidationError('The given URL does not match valid image extensions.')
        return url

    # def save(self, force_insert=False, force_update=False, commit=True):
    #     image = super(ImageCreateForm, self).save(commit=False)
    #     image_url = self.cleaned_data['url']
    #     image_name = '{}.{}'.format(slugify(image.title), image_url.rsplit('.',1)[1].lower())
    #
    #     response = request.urlopen(image_url)
    #     image.image.save(image_name, ContentFile(response.read()), save=False)
    #
    #     if commit:
    #         image.save()
    #     return image

class CommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs=
                {"name":"body", "class":"form-control" ,"id":"message" ,"rows":"3" ,"placeholder":"What are you thinking?"}
                    )
                )
    class Meta:
        model = Comment
        exclude = ('content_type', 'object_id', 'content_object')
