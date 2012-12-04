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
from django.db.models import Count
import time
import uuid, hashlib
import simplejson as json
import random
from game.assimilation import Assimilation, Tile
import HTMLParser
from assimilation.models import *

def getUserStats(user):
	try:
		games = Game.objects.filter(gameuser__user=user.id)
		complete = games.filter(status='complete')
	except Game.DoesNotExist:
		pass
	try:
		wins = GameUser.objects.filter(user=user.id).filter(won=True)
	except GameUser.DoesNotExist:
		pass
	user.totalGames = len(games)
	user.completeGames = len(complete)
	user.totalWins = len(wins)
	user.totalLosses = user.completeGames - user.totalWins
	if user.completeGames > 0:
		user.winPercent = int((float(user.totalWins)/float(user.completeGames))*100)
	else:
		user.winPercent = 0
	places = {}
	try:
		winCounts = GameUser.objects.filter(won=True).values('user').annotate(Count('user'))
		counts = list(winCounts)
		counts.sort(key=lambda winner: winner['user__count'], reverse=True)
		places[0] = len(counts)+1
		for i in range(len(counts)-1,-1,-1):
			places[counts[i]['user__count']] = i+1
		print places
	except GameUser.DoesNotExist:
		pass
	user.rank = places[user.totalWins]
	return user

@login_required
def index(request):
	user = getUserStats(request.user)
	return render_to_response('game/index.html',{'user': user}, context_instance=RequestContext(request))

@login_required
def games(request):
	user = getUserStats(request.user)
	return render_to_response('game/games.html',{'user':user}, context_instance=RequestContext(request))

@login_required
def play(request, id):
	try:
		game = Game.objects.filter(gameuser__user = request.user.id).get(pk=id)
	except Game.DoesNotExist:
		return HttpResponseRedirect(reverse('assimilation.views.games'))	
	user = getUserStats(request.user)
	return render_to_response('game/play.html',{'game':game, 'size': range(1,game.size+1), 'compiled': False, 'user':user}, context_instance=RequestContext(request))

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
		create = UserForm()
		return render_to_response('auth/login.html', {'form':form, 'create':create, 'login':True}, context_instance=RequestContext(request))

	if request.method == 'POST':
		form = LoginForm(request.POST)
		if not form.is_valid():
			return render_to_response('auth/login.html', {'form':form, 'login':True}, context_instance=RequestContext(request))

		user = authenticate(username=request.POST['username'], password=request.POST['password'])

		if user is None:
			return render_to_response('auth/login.html', {'form':form, 'error':'Invalid username or password', 'login':True}, context_instance=RequestContext(request))
		django.contrib.auth.login(request,user)
		return HttpResponseRedirect(request.session['next'])

def create(request):
	if request.method == 'GET':
		form = UserForm()
		signin = LoginForm()
		return render_to_response('auth/login.html', {'form':signin, 'create':form}, context_instance=RequestContext(request))

	if request.method == 'POST':
		form = UserForm(request.POST)
		signin = LoginForm()
		if not form.is_valid():
			return render_to_response('auth/login.html', {'form':signin, 'create':form}, context_instance=RequestContext(request))

		try:
			u = User.objects.get(username=form.cleaned_data['username'])
			return render_to_response('auth/login.html', {'form':signin, 'create':form, 'create_error':'Username already taken'}, context_instance=RequestContext(request))
		except User.DoesNotExist:
			pass
		try:
			e = User.objects.get(email=form.cleaned_data['email'])
			return render_to_response('auth/login.html', {'form':signin, 'create':form, 'create_error':'Email already in use.'}, context_instance=RequestContext(request))
		except User.DoesNotExist:
			pass

		if request.POST['password'] != request.POST['confirm']:
			return render_to_response('auth/login.html', {'form':signin, 'create':form, 'create_error':'Passwords do not match.'}, context_instance=RequestContext(request))

		user = User.objects.create_user(form.cleaned_data['username'], form.cleaned_data['email'], form.cleaned_data['password'])
		user.first_name = form.cleaned_data['name']
		user.save()
		newUser = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
		django.contrib.auth.login(request,newUser)
		return HttpResponseRedirect(reverse('assimilation.views.index'))

def logout(request):
	django.contrib.auth.logout(request)
	return HttpResponseRedirect(reverse('assimilation.views.index'))

@login_required
def update(request):
	if request.method == 'POST':
		post = request.POST
		name = post.get('name',False)
		email = post.get('email',False)
		password = post.get('password',False)
		newpassword = post.get('new-password',False)
		newpassagain = post.get('new-pass-again',False)
		user = authenticate(username=request.user.username, password=password)
		if user is None:
			return HttpResponse('{"success":false, "error":"Invalid Password"}', mimetype="application/json")

		if name:
			user.first_name = name
		if email:
			try:
				e = User.objects.get(email=email)
				if e.id != user.id:
					return HttpResponse('{"success":false, "error":"Email already in use"}', mimetype="application/json")
			except User.DoesNotExist:
				pass
			user.email = email
		if newpassword or newpassagain:
			if newpassagain != newpassword:
				return HttpResponse('{"success":false, "error":"New Passwords do not match"}', mimetype="application/json")
			user.set_password(newpassword)
		user.save()
		return HttpResponse('{"success":true}', mimetype="application/json")

	return HttpResponse('{"success":false,"error":"Must POST to update account"}', mimetype="application/json")



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
def usergames(request):
	user_id = request.user.id
	userTime = datetime.fromtimestamp(float(request.GET.get('time',0)))
	# games = [];
	try:
		# gameUsers = GameUser.objects.filter(user = user_id)
		print 'trying to get games'
		games = Game.objects.filter(gameuser__user=user_id).filter(updated__gt=userTime)
		print len(games)		
		for game in games:
			game.users = game.gameuser_set.all()
			game.playerState = {}
			if game.status != 'init':
				temp = Assimilation(JSON=game.state)
				game.playerState = temp.getStateFor(user_id)
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
		chats = Message.objects.all().order_by("-pk")
		index = 0
		if len(chats)>0:
			index = chats[0].id
		return render_to_response('ajax/chats.json',{'last_message': index, 'messages': messages, 'users':users}, mimetype='application/json', context_instance=RequestContext(request))

	if request.method == "POST":
		content = request.POST.get('content','')
		if(len(content) == 0):
			return HttpResponseBadRequest('Need to POST content to create a message')
		new_message = Message()
		new_message.text = content.replace("\\","\\\\").replace("\n","\\n").replace("\t","\\t")
		new_message.user = request.user
		new_message.game = Game.objects.get(pk=game_id)
		new_message.save()
		return render_to_response('ajax/chats.json',{'success': True}, mimetype='application/json', context_instance=RequestContext(request))

@login_required
def getgame(request, game_id):
	if request.method == 'GET':
		updated = datetime.fromtimestamp(float(request.GET.get('updated',0)))
		try:
			game = Game.objects.get(pk=game_id, updated__gt=updated)
			game.users = game.gameuser_set.all()
		except Game.DoesNotExist:
			return HttpResponse('{"success":true}', mimetype="application/json")
		if game.state == 'init':
			return render_to_response('ajax/game.json', {"game":game}, context_instance=RequestContext(request))

		temp = Assimilation(JSON=game.state)
		state = temp.getStateFor(request.user.id, True)
		return render_to_response('ajax/game.json', {"game":game, "state":state}, context_instance=RequestContext(request))

	return HttpResponse('{"success":false, "error":"cannot use ' + request.method + '"}', mimetype="application/json")


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
		game.updated = datetime.now()
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
		game.updated = datetime.now()
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


def placetile(request, game_id):
	if request.is_ajax():
		try:
			game = Game.objects.get(pk=game_id)
		except:
			return HttpResponse('{"success":false, "error":"Game does not exist"}', mimetype="application/json")

		if game.activePlayer.id != request.user.id:
			return HttpResponse('{"success":false, "error":"Not your turn"}', mimetype="application/json")

		post = request.POST
		x = request.POST.get('x', None)
		y = request.POST.get('y', None)
		if x is None or y is None:
			return HttpResponse('{"success":false, "error":"Need to submit a tile"}', mimetype="application/json")

		model = Assimilation(JSON=game.state)
		if not model.placeTile(Tile(x,y), request.user.id):
			return HttpResponse('{"success":false, "error":"Invalid move submission"}', mimetype="application/json")

		game.state = model.export()
		for player in model.players:
			p = game.gameuser_set.get(user=player.id)
			p.score = player.score
			p.save()
		game.activePlayer = game.gameuser_set.exclude(user=game.activePlayer)[0].user
		game.updated = datetime.now()
		if model.status == 'complete':
			game.status = 'complete'
			for player in model.players:
				if player.score > 0:
					p = game.gameuser_set.get(user = player.id)
					p.won = True
					p.save()
		game.save()

		return HttpResponse('{"success":true}', mimetype="application/json")
	raise Http404

def resign(request, game_id):
	if request.is_ajax():
		try:
			game = Game.objects.get(pk=game_id)
		except:
			return HttpResponse('{"success":false, "error":"Game does not exist"}', mimetype="application/json")

		if game.activePlayer.id != request.user.id:
			return HttpResponse('{"success":false, "error":"Not your turn"}', mimetype="application/json")

		model = Assimilation(JSON = game.state)
		model.resign(request.user.id)
		game.state = model.export()
		for player in model.players:
			p = game.gameuser_set.get(user=player.id)
			p.score = player.score
			p.save()

		if model.status == 'complete':
			game.status = 'complete'
			for player in model.players:
				if player.score > 0:
					p = game.gameuser_set.get(user = player.id)
					p.won = True
					p.save()
		game.updated = datetime.now()
		game.save()
		return HttpResponse('{"success":true}', mimetype="application/json")
	raise Http404 

def swap(request, game_id):
	if request.is_ajax():
		try:
			game = Game.objects.get(pk=game_id)
		except:
			return HttpResponse('{"success":false, "error":"Game does not exist"}', mimetype="application/json")

		if game.activePlayer.id != request.user.id:
			return HttpResponse('{"success":false, "error":"Not your turn"}', mimetype="application/json")

		post = request.POST
		tiles = post.get('swap','[]')
		tiles = json.loads(tiles)
		swap = []
		for tile in tiles:
			swap.append(Tile(tile['x'],tile['y']))
		model = Assimilation(JSON=game.state)
		if not model.swapTiles(swap, request.user.id):
			return HttpResponse('{"success":false, "error":"Invalid tile submission"}', mimetype="application/json")

		game.state = model.export()
		game.activePlayer = game.gameuser_set.exclude(user=game.activePlayer)[0].user
		game.updated = datetime.now()
		game.save()

		return HttpResponse('{"success":true}', mimetype="application/json")
	raise Http404