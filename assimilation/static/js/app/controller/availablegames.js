goog.provide('assimilation.AvailableGames');
goog.require('assimilation.JoinGameDialog');
goog.require('a.util');

/**
* @constructor
*/
assimilation.AvailableGames = function(){
	this.container = $('.available-games-list');
	this.games = [];
	this.container.empty();
	this.update();
	this.joinGameDialog = new assimilation.JoinGameDialog();
}

assimilation.AvailableGames.prototype.addGameToList = function(player, playercolor, size, created, password, id) {
	var me = this;
	var newItem = $('<div>').addClass('available-game');
	var creator = $('<div>').addClass('creator');
	var name = $('<div>').addClass('name').text(player);
	var color = $('<div>').addClass('color').addClass(playercolor);
	var info = $('<div>').addClass('game-info');
	var headers = ['size','created','password?'];
	var table = $('<table>');
	var row1 = $('<tr>');
	var row2 = $('<tr>');
	for(var i=0; i<headers.length; i++){
		row1.append($('<td>').addClass('info-name').text(headers[i]));
	}
	row2.append($('<td>').addClass('info-content').text(size + 'x' + size));
	row2.append($('<td>').addClass('info-content').text(created));
	row2.append($('<td>').addClass('info-content').text(password ? "Yes" : "No"));
	table.append(row1);
	table.append(row2);
	var button = $('<div>').addClass('join').text('Join');
	button.click(function(){
		me.joinGame(id, player, playercolor, password);
	});
	creator.append(name).append(color);
	info.append(table);
	newItem.append(creator).append(info).append(button);
	this.container.append(newItem);
};

assimilation.AvailableGames.prototype.update = function() {
	var me = this;
	$.ajax('/assimilation/game/available',{
		'type':'GET',
		'dataType':'json',
		'success': function(response){
			var games = response['games'];
			for(var i=0; i<games.length; i++){
				me.addGameToList(games[i]['player'],games[i]['color'],games[i]['size'],games[i]['created'].substr(0,8),games[i]['password'],games[i]['id'])
			}
		}
	});
};

assimilation.AvailableGames.prototype.joinGame = function(id, player, playercolor, password) {
	this.joinGameDialog.show(id, player, playercolor, password);
};