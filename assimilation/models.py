from django.contrib.auth.models import User
from django.db import models
from django import forms

# Create your models here.
class Game(models.Model):
	# id = models.CharField('id', max_length=40, primary_key=True)
	created = models.DateTimeField('Date Created', auto_now_add=True)
	creator = models.ForeignKey(User)
	size = models.IntegerField('Size')
	updated = models.DateTimeField('Updated', null=True)
	status = models.CharField('Status', max_length=10)
	state = models.CharField('State', max_length=1000000)
	password = models.CharField('Password', max_length=100, null=True)
	salt = models.CharField('Salt', max_length=20, null=True)

class GameUser(models.Model):
	user = models.ForeignKey(User)
	game = models.ForeignKey(Game)
	color = models.CharField('Color', max_length=10)
	won = models.BooleanField('Won')

class Message(models.Model):
	user = models.ForeignKey(User)
	game = models.ForeignKey(Game)
	text = models.CharField('Text', max_length=1000)
	created = models.DateTimeField('Date Created', auto_now_add=True)

class LoginForm(forms.Form):
	username = forms.CharField(max_length=100)
	password = forms.CharField(widget=forms.PasswordInput(render_value=False), max_length=100)

class UserForm(forms.Form):
	username = forms.CharField(max_length=100)
	email = forms.EmailField(max_length=100)
	name = forms.CharField(max_length=100)
	password = forms.CharField(widget=forms.PasswordInput(render_value=False), max_length=100)
	confirm = forms.CharField(widget=forms.PasswordInput(render_value=False), max_length=100)