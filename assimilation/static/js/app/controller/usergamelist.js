goog.provide('assimilation.UserGameList');
goog.require('assimilation.Board');
goog.require('a.util');
/**
*
* @constructor
*/
assimilation.UserGameList = function(userid){
	this.userid = userid;
	this.container = $('.game-list');
	this.container.empty();
	this.update();
	this.games = {};
	this.time = 0;
	this.board = new assimilation.Board();
}


assimilation.UserGameList.prototype.update = function() {
	var me = this;
	var data = {
		'time':this.time
	};
	$.ajax('/assimilation/usergames/', {
		'success': function(data){
			me.time = data['time'];
			var games = data['games'];
			if(games.length > 0){
				for(var i=0; i<games.length; i++){
					me.addGame(games[i]);
				}
				me.displayGames();
			}
			// setTimeout(function() {me.update();}, 2000);
		},
		'dataType':'json',
		'data':data,
		'type':'GET'
	});
};

assimilation.UserGameList.prototype.displayGames = function() {
	var games = [];
	for(id in this.games){
		games.push(this.games[id]);
	}
	games.sort(function(a,b){
		if(a['status'] < b['status']){
			return 1;
		}else if(a['status'] > b['status']){
			return -1;
		}
		else{
			if(a['status'] == 'playing'){
				if(a['myTurn'] && !b['myTurn'])
					return -1;
				if(!a['myTurn'] && b['myTurn'])
					return 1;
				return Number(a['updated']) - Number(b['updated']);
			}
			else{
				return Number(b['updated']) - Number(a['updated']);
			}
		}
	});
	for(var i=0; i<games.length; i++)
		this.container.append(games[i].dom);
};

assimilation.UserGameList.prototype.addGame = function(game) {
	var me=this;
	if(this.games[game['id']]){
		this.games[game['id']]['dom'].remove();
	}
	var newGameContainer = $("<div>").addClass('game-list-item');
	var users = {};
	if(game['status'] == 'playing'){
		var left = $('<div>').addClass('game-item-left');
		var players = $('<div>').addClass('players').append($('<div>').addClass('players-title').text('Players'));	
		var list = $('<ul>');
		for(var i=0; i<game.users.length; i++){
			var user = game.users[i];
			var li = $('<li>').addClass(user['color']);
			if(user['id'] == game['currentPlayer'])
				li.addClass('active');
			li.text(user['name']);
			list.append(li);
			users[user['id']] = user;
		}
		players.append($('<div>').addClass('player-list').append(list));

		players.append($('<div>').addClass('last-move').text('Last Move:').append($('<span>').text(moment(new Date(Math.floor(1000*Number(game['updated'])))).fromNow())));

		left.append(players);

		var right = $("<div>").addClass('game-item-right');
		var status = $('<div>').addClass('status');
		var button = $('<div>').addClass('action-button');
		if(this.userid == game['currentPlayer']){
			status.addClass('green');
			status.text('Your Turn!');
			button.text('Play');
		}
		else{
			status.addClass('red');
			status.text('Waiting');
			button.text('View')
		}
		right.append(status).append(button);
		newGameContainer.append(left);
		newGameContainer.append(right);

		button.click(function(e){
			e.stopPropagation();
			window.location.pathname='/assimilation/play/' + game.id;
		});

	}
	else if(game['status'] == 'init'){
		var message = $('<div>').addClass('message').text('Waiting for opponent to join.');
		var deleteButton = $('<div>').addClass('delete').text('Delete Game');
		deleteButton.click(function(e){
			e.stopPropagation();
			$.ajax('/assimilation/game/delete/' + game.id, {
				'success': function(info){
					if(info['success']){
						newGameContainer.remove();
					}
					else{
						if(info['error'])
							alert(info['error']);
					}
				}
			})
		});
		newGameContainer.append(message).append(deleteButton);
	} else if(game['status'] == 'complete'){
		var left = $('<div>').addClass('game-item-left');
		var players = $('<div>').addClass('players').append($('<div>').addClass('players-title').text('Players'));	
		var list = $('<ul>');
		for(var i=0; i<game.users.length; i++){
			var user = game.users[i];
			var li = $('<li>').addClass(user['color']);
			if(user['won'])
				li.addClass('active');
			li.text(user['name']);
			list.append(li);
			users[user['id']] = user;
		}
		players.append($('<div>').addClass('player-list').append(list));

		players.append($('<div>').addClass('last-move').text('Last Move:').append($('<span>').text(moment(new Date(Math.floor(1000*Number(game['updated'])))).fromNow())));

		left.append(players);

		var right = $("<div>").addClass('game-item-right');
		var status = $('<div>').addClass('status');
		var button = $('<div>').addClass('action-button');
		status.addClass('green');
		status.text('Complete');
		button.text('View')
		right.append(status).append(button);
		newGameContainer.append(left);
		newGameContainer.append(right);

		button.click(function(e){
			e.stopPropagation();
			window.location.pathname='/assimilation/play/' + game.id;
		});		
	}
	
	this.games[game['id']] = {
		'dom':newGameContainer,
		'state': game['state'],
		'players': users,
		'myTurn' : this.userid == game['currentPlayer'],
		'size': game['size'],
		'status': game['status'],
		'updated': game['updated']
	};
	newGameContainer.click(function(){
		$('.game-list-item').removeClass('selected');
		newGameContainer.addClass('selected');
		me.showGame(game['id']);
	});
};

assimilation.UserGameList.prototype.showGame = function(id) {
	var state = this.games[id]['state'];
	var players = this.games[id]['players'];
	var size = this.games[id]['size'];
	this.board.showState(state,players, size);
};