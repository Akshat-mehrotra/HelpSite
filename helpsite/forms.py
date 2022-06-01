from django.forms import ModelForm
from django.conf import settings
from django.template.defaultfilters import filesizeformat

from .models import Post

class PostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ('creation_date',)


    def clean(self):
        cleaned_data = super().clean()
        
        phone = cleaned_data.get('phone')
        if not (cleaned_data.get('instagram') or cleaned_data.get('email') or phone):
            msg = "atleast one of these should be valid"
            self.add_error('phone', msg)
            self.add_error('instagram', msg)
            self.add_error('email', msg)

        if phone:
            if not phone.isnumeric():
                self.add_error('phone', "Phones can't have non numbers :(")
       
        if not (cleaned_data.get('PH') or cleaned_data.get('price')):
            msg = "You must provide either $ or $/Hr"
            self.add_error('PH', msg)
            self.add_error('price', msg)

        attach = cleaned_data.get('attachment')
        if attach:
            if attach.size > settings.MAX_UPLOAD_SIZE:
                self.add_error('attachment', f'Please keep filesize under {filesizeformat(settings.MAX_UPLOAD_SIZE)}. Current filesize {filesizeformat(attach.size)}')
        
class questionPasswordForm(ModelForm):
    class Meta:
        model = Post
        fields = ['password']