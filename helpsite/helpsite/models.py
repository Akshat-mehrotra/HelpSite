from ast import Mod
from django.db import models
from django.forms import ModelForm
from sqlalchemy import true

from classes import classes, courses
from supportedschools import schools

class Post(models.Model):
    ip = models.GenericIPAddressField()
    subject = models.CharField(max_length=100, choices=classes)
    course = models.CharField(max_length = 100, null=True, blank=True, )
    desc = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    contact = models.CharField(max_length=100)
    school = models.CharField(max_length=100)
    attach = models.FileField(upload_to='attachments/', blank=True, null=True)
    price = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    PH = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    solved = models.BooleanField(default=False)

    def __str__(self) -> str:
          return f"By: {self.ip},\nsubject: {self.subject},\ncourse: {self.course},\ndesc: {self.desc}\nschool: {self.school}"
    
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