import os 

from django.db import models
from django.forms import ModelForm
from django.forms import ValidationError
from django.core.validators import MinLengthValidator, FileExtensionValidator
from django.conf import settings
from django.template.defaultfilters import filesizeformat

from classes import classes, courses
from supportedschools import schools

class Post(models.Model):
    ip = models.GenericIPAddressField()
    subject = models.CharField(max_length=100, choices=classes)
    course = models.CharField(max_length = 100, null=True, blank=True, )
    desc = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    instagram = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=250, null=True, blank=True)
    phone = models.CharField(max_length=10, validators=[MinLengthValidator(10),], null=True, blank=True)
    school = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    PH = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    solved = models.BooleanField(default=False)
    attachment = models.FileField(upload_to='attachments/', null=True, blank=True, validators=[FileExtensionValidator(['pdf', 'jpg', 'png', 'jpeg'])])

    def __str__(self) -> str:
          return f"By: {self.ip},\nsubject: {self.subject},\ncourse: {self.course},\ndesc: {self.desc}\nsolved: {self.solved}"
    
    def save(self, *args, **kwargs):
        assert self.school in schools, f"{self.school} not supported :("
        if self.course:
            assert self.course in courses[self.subject], f"Course {self.course} not in Subject {self.subject}"

        assert self.PH or self.price, "Price not specified, nor per hour rate."
        super(Post, self).save(*args, **kwargs)

class PostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ('ip', 'creation_date')

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
        
