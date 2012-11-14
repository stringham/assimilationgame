goog.provide('assimilation.UserGameList');

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
}


assimilation.UserGameList.prototype.update = function() {
	var me = this;
	$.ajax('/assimilation/usergames/' + this.userid, {
		'success': function(data){
			me.time = data['time'];
			var games = data['games'];
			for(var i=0; i<games.length; i++){
				me.addGame(games[i]);
			}
		},
		'dataType':'json'
	});
};

assimilation.UserGameList.prototype.addGame = function(game) {
	if(this.games[game['id']]){
		this.games[game['id']].remove();
	}
	var newGameContainer = $("<div>").addClass('game-list-item');
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
	}
	players.append($('<div>').addClass('player-list').append(list));

	players.append($('<div>').addClass('last-move').text('Last Move:').append($('<span>').text(game['updated'].substr(0,7))))

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
	this.games[game['id']] = newGameContainer;
	this.container.append(newGameContainer);

	button.click(function(e){
		e.stopPropagation();
		window.location.pathname='/assimilation/play/' + game.id;
	});

	newGameContainer.click(function(){
		$('.game-list-item').removeClass('selected');
		newGameContainer.addClass('selected');
	});
};