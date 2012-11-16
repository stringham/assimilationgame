# Create your views here.
import django.contrib.auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404, HttpResponseBadRequest, HttpResponse
from django.template import RequestContext
from django.utils import simplejson
from django.shortcuts import render_to_response
from datetime import datetime
import time
import uuid, hashlib
import simplejson as json
import random
from game.assimilation import Assimilation
import HTMLParser
from assimilation.models import *

@login_required
def index(request):
	return render_to_response('game/index.html',{}, context_instance=RequestContext(request))

@login_required
def games(request):
	return render_to_response('game/games.html',{'user':request.user})

@login_required
def play(request, id):
	try:
		game = Game.objects.get(pk=id)
	except Game.DoesNotExist:
		return HttpResponseRedirect(reverse('assimilation.views.games'))

	return render_to_response('game/play.html',{'user':request.user, 'game':game})

@login_required
def delete(request, id):
	try:
		i = Item.objects.get(pk=id)
	except Item.DoesNotExist:
		raise Http404
	remove_today(i)
	i.delete()
	return HttpResponseRedirect(reverse('assimilation.views.index'))

def login(request):
	if request.method == 'GET':
		form = LoginForm()
		request.session['next'] = request.GET['next']
		return render_to_response('auth/login.html', {'form':form, 'login':True}, context_instance=RequestContext(request))

	if request.method == 'POST':
		form = LoginForm(request.POST)
		if not form.is_valid():
			return render_to_response('auth/login.html', {'form':form, 'login':True}, context_instance=RequestContext(request))

		user = authenticate(username=request.POST['username'], password=request.POST['password'])

		if user is None:
			return render_to_response('auth/login.html', {'form':form, 'error':'Invalid username or password', 'login':True}, context_instance=RequestContext(request))
		django.contrib.auth.login(request,user)
		return HttpResponseRedirect(request.session['next'])

def logout(request):
	django.contrib.auth.logout(request)
	return HttpResponseRedirect(reverse('assimilation.views.index'))

def create(request):
	if request.method == 'GET':
		form = UserForm()
		return render_to_response('auth/create.html', {'form':form}, context_instance=RequestContext(request))

	if request.method == 'POST':
		form = UserForm(request.POST)
		if not form.is_valid():
			return render_to_response('auth/create.html', {'form':form}, context_instance=RequestContext(request))

		try:
			u = User.objects.get(username=form.cleaned_data['username'])
			return render_to_response('auth/create.html', {'form':form, 'error':'Username already taken'}, context_instance=RequestContext(request))
		except User.DoesNotExist:
			pass
		try:
			e = User.objects.get(email=form.cleaned_data['email'])
			return render_to_response('auth/create.html', {'form':form, 'error':'Email already in use.'}, context_instance=RequestContext(request))
		except User.DoesNotExist:
			pass

		if request.POST['password'] != request.POST['confirm']:
			return render_to_response('auth/create.html', {'form':form, 'error':'Passwords do not match.'}, context_instance=RequestContext(request))

		user = User.objects.create_user(form.cleaned_data['username'], form.cleaned_data['email'], form.cleaned_data['password'])
		user.first_name = form.cleaned_data['name']
		user.save()
		return HttpResponseRedirect(reverse('assimilation.views.index'))

def makeadmin(request):
	# try:
	# 	u = User.objects.get(pk=request.user.id)
	# 	u.is_staff = True
	# 	u.is_superuser = True
	# 	u.save();
	# 	return HttpResponseRedirect(reverse('assimilation.views.index'))
	# except User.DoesNotExist:
	return HttpResponseRedirect(reverse('assimilation.views.index'))


def get_today(request):
	if not request.session.has_key('today'):
		request.session['today'] = []
	return request.session['today']

def add_today(request, item):
	l = get_today(request)
	if item not in l:
		l.append(item)
		request.session.modified = True

def remove_today(request, item):
	l = get_today(request)
	if item in l:
		l.remove(item)
		request.session.modified = True

@login_required
def today(request, id):
	try:
		i = Item.objects.get(pk=id)
	except Item.DoesNotExist:
		raise Http404
	if i.user_id != request.user.id:
		raise Http404
	add_today(request, i)
	return HttpResponseRedirect(reverse('assimilation.views.index'))

@login_required
def later(request, id):
	try:
		i = Item.objects.get(pk=id)
	except Item.DoesNotExist:
		raise Http404
	if i.user_id != request.user.id:
		raise Http404
	remove_today(request, i)
	return HttpResponseRedirect(reverse('assimilation.views.index'))

@login_required
def usergames(request, user_id):
	userTime = datetime.fromtimestamp(float(request.GET.get('time',0)))
	games = [];
	try:
		gameUsers = GameUser.objects.filter(user = user_id)
		for entry in gameUsers:
			game = Game.objects.get(pk=entry.game.id)
			game.users = game.gameuser_set.all()
			games.append(game)
	except GameUser.DoesNotExist:
		pass

	return render_to_response('ajax/userlist.json', {'current_unix_timestamp': time.time(), 'games':games}, context_instance=RequestContext(request))

def availablegames(request):
	userTime = datetime.fromtimestamp(float(request.GET.get('time',0)))
	# games = [];
	try:
		games = Game.objects.filter(status="init")
		for game in list(games):
			game.color = game.gameuser_set.get(user = game.creator).color
	except Game.DoesNotExist:
		pass

	return render_to_response('ajax/availablelist.json', {'current_unix_timestamp': time.time(), 'games':games}, context_instance=RequestContext(request))

@login_required
def chats(request, game_id):
	if request.method == "GET":
		requestedId = int(request.GET.get('last_message',0))
		try:
			messages = Message.objects.filter(id__gt=requestedId).filter(game=game_id)
		except Message.DoesNotExist:
			render_to_response('ajax/chats.json', {}, context_instance=RequestContext(request))
		try:	
			users = GameUser.objects.filter(game=game_id)
		except GameUser.DoesNotExist:
			pass
		return render_to_response('ajax/chats.json',{'last_message': Message.objects.all().order_by("-pk")[0].id, 'messages': messages, 'users':users}, mimetype='application/json', context_instance=RequestContext(request))

	if request.method == "POST":
		content = request.POST.get('content','')
		# print request.POST
		if(len(content) == 0):
			return HttpResponseBadRequest('Need to POST content to create a message')
		new_message = Message()
		new_message.text = content.replace("\\","\\\\").replace("\n","\\n").replace("\t","\\t")
		new_message.user = request.user
		new_message.game = Game.objects.get(pk=game_id)
		new_message.save()
		return render_to_response('ajax/chats.json',{'success': True}, mimetype='application/json', context_instance=RequestContext(request))

@login_required
def creategame(request):
	if request.method == "POST":
		post = request.POST
		size = int(post.get('size',0))
		color = post.get('color','')
		password = post.get('password','')
		if size not in [8,10,12]:
			return render_to_response('ajax/creategame.json',{'success':"false", 'error':'invalid size submitted'})
		if color not in ['blue','green','yellow','orange','red','teal']:
			return render_to_response('ajax/creategame.json',{'success':"false", 'error':'invalid color submitted'})
		game = Game()
		game.creator = request.user
		game.size = size
		game.status = "init"
		game.state = "{}"
		game.updated = None
		game.activePlayer = None
		if len(password) > 0:
			salt = uuid.uuid1().hex[:20]
			password_hash = hashlib.sha384(salt + password).hexdigest()
			game.salt = salt
			game.password = password_hash
		else:
			game.password = None
			game.salt = None
		game.save()
		player = GameUser()
		player.user = request.user
		player.game = game
		player.color = color
		player.score = 0
		player.won = False
		player.save()
		return render_to_response('ajax/creategame.json',{'success':"true", 'id':game.id}, context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect(reverse('assimilation.views.index'))

@login_required
def joingame(request, game_id):
	if request.method == "POST":
		post = request.POST
		color = post.get('color','')
		password = post.get('password','')
		print password
		try:
			game = Game.objects.get(pk=game_id)
		except Game.DoesNotExist:
			return HttpResponse('{"success":false, "error":"Game does not exist"}', mimetype="application/json")
		if game.status != "init":
			return HttpResponse('{"success":false, "error":"Can\'t join this game"}', mimetype="application/json")
		if game.password:
			if hashlib.sha384(game.salt + password).hexdigest() != game.password:
				return HttpResponse('{"success":false, "error":"Invalid password"}', mimetype="application/json")
		if game.creator == request.user:
			return HttpResponse('{"success":false, "error":"Can\'t join your own game"}', mimetype="application/json")
		colors = ['blue','green','yellow','orange','red','teal']
		remove = game.gameuser_set.get(user=game.creator).color
		colors.remove(remove)
		if color not in colors:
			return HttpResponse('{"success":false, "error":"invalid color submitted"}', mimetype="application/json")

		game.status = "playing"
		game.activePlayer = game.creator if random.random() < 0.5 else request.user
		g = Assimilation(game.id, game.size, [request.user.id,game.creator.id])
		game.state = g.export()
		game.save()
		player = GameUser()
		player.game = game
		player.color = color
		player.user = request.user
		player.score = 0
		player.won = False
		player.save()
		return HttpResponse('{"success":true}', mimetype="application/json")
	else:
		raise Http404

def deletegame(request, game_id):
	if request.is_ajax():
		try:
			game = Game.objects.get(pk=game_id)
		except:
			return HttpResponse('{"success":false, "error":"Game does not exist"}', mimetype="application/json")

		if game.status != "init":
			return HttpResponse('{"success":false, "error":"Can only delete games that haven\'t started yet"}', mimetype="application/json")

		game.delete()

		return HttpResponse('{"success":true}', mimetype="application/json")
	raise Http404
