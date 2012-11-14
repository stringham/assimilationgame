# Create your views here.
import django.contrib.auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404, HttpResponseBadRequest
from django.template import RequestContext
from django.utils import simplejson
from django.shortcuts import render_to_response
from datetime import datetime
import time
import uuid, hashlib


from assimilation.models import *

@login_required
def index(request):
	list = [{'color':'teal','name':'Ryan'},{'color':'red','name':'Paul'},{'color':'green','name':'Sarah'},{'color':'blue','name':'Kesler'},{'color':'yellow','name':'Kameron'}]
	return render_to_response('game/index.html',{'list':list, 'user':request.user})

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


@login_required
def chats(request, game_id):
	if request.method == "GET":
		for x in range(90):
			userTime = datetime.fromtimestamp(float(request.GET.get('time',0)))
			try:
				messages = Message.objects.filter(created__gt=userTime).filter(game=game_id)
			except Message.DoesNotExist:
				render_to_response('ajax/chats.json', {'current_unix_timestamp': time.time()})
			try:	
				users = GameUser.objects.filter(game=game_id)
			except GameUser.DoesNotExist:
				pass
			if(len(list(messages))>0):
				return render_to_response('ajax/chats.json',{'current_unix_timestamp': time.time(), 'messages': messages, 'users':users, 'usertime':userTime}, context_instance=RequestContext(request))
			time.sleep(.5)
		return render_to_response('ajax/chats.json',{'current_unix_timestamp': time.time(), 'messages': messages, 'users':users, 'usertime':userTime}, context_instance=RequestContext(request))

	if request.method == "POST":
		content = request.POST.get('content','')
		# print request.POST
		if(len(content) == 0):
			return HttpResponseBadRequest('Need to POST content to create a message')
		new_message = Message()
		new_message.text = content
		new_message.user = request.user
		new_message.game = Game.objects.get(pk=game_id)
		new_message.save()
		return render_to_response('ajax/chats.json',{'success': True}, context_instance=RequestContext(request))

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