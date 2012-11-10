from django.contrib.auth.models import User
from django.db import models
from django import forms

# Create your models here.
class Item(models.Model):
	user = models.ForeignKey(User)
	text = models.CharField('Text', max_length=200)
	created = models.DateTimeField('Date Created', auto_now_add=True)

class ItemForm(forms.ModelForm):
	class Meta:
		model = Item

class LoginForm(forms.Form):
	username = forms.CharField(max_length=100)
	password = forms.CharField(widget=forms.PasswordInput(render_value=False), max_length=100)

class UserForm(forms.Form):
	username = forms.CharField(max_length=100)
	email = forms.EmailField(max_length=100)
	name = forms.CharField(max_length=100)
	password = forms.CharField(widget=forms.PasswordInput(render_value=False), max_length=100)
	confirm = forms.CharField(widget=forms.PasswordInput(render_value=False), max_length=100)