goog.provide('assimilation.Play');
goog.require('assimilation.Chats');
goog.require('assimilation.Board');
goog.require('assimilation.Game');
goog.require('a.util');

/**
* @constructor
*/
assimilation.Play = function(gameid){
	var me = this;
	this.board = new assimilation.Board();
	this.chats = new assimilation.Chats(gameid);
	this.gameid = gameid;
	this.showingHistoric = false;
	this.playersContainer = $('.player-content');
	this.playersContainer.empty();
	this.players = {};
	this.history = [];
	this.historyContainer = $('.history-list');
	this.historyContainer.empty().mouseleave(function(){
		if(me.showingHistoric){
			me.updateBoard();
			me.updatePieces();
			me.showingHistoric = false;
		}
	});

	this.piecesContainer = $('.pieces');
	this.piecesContainer.empty();

	this.modified = 0;

	this.update();
}


assimilation.Play.prototype.update = function() {
	var me = this;
	var data = {
		'updated': this.modified
	};
	$.ajax('/assimilation/game/get/' + this.gameid,{
		'type':'GET',
		'dataType':'json',
		'data':data,
		'success':function(res){
			if(res['game']){
				if(me.modified != res['game']['updated']){
					me.game = res['game'];
					me.updatePlayers();
					me.updateHistory();
					me.updateBoard();
					me.updatePieces();
					me.modified = me.game['updated'];
				}
				setTimeout(function() {
					me.update();
				}, 1000);
			}
			else if(res['success']){
				setTimeout(function() {
					me.update();
				}, 1000);
			}
		},
		'failure':function(res){
		}
	})
};

assimilation.Play.prototype.updatePlayers = function() {
	var players = this.game['users'];
	this.playersContainer.empty();
	for(var i=0; i<players.length; i++){
		var player = players[i];
		this.players[player.id] = player;
		var container = $('<div>').addClass('player');
		var name = $('<div>').addClass('name').text(player['name']);
		var score = $('<div>').addClass('player-piece').addClass(player['color']).text(player['score']);
		if(player['id'] == this.game['currentPlayer'])
			score.addClass('active');
		container.append(name).append(score);
		this.playersContainer.append(container);
	}
};

function getTileName(tile){
	return String.fromCharCode(65 + tile.x) + (tile.y+1);
}

assimilation.Play.prototype.updateHistory = function() {
	var history = this.game['state']['h'];
	var claim;
	var me = this;
	a.util.map(history, function(claim, i){
		if(!me.history[i+1]){
			var number = $('<div>').addClass('number').text(i+1);
			var move = $('<div>').addClass('move').addClass(me.players[claim.o].color).text(getTileName(claim.t)).click(function(){
				me.showHistoricState(i+1);
			});
			me.historyContainer.append(number).append(move);
			me.history[i+1] = move;
		}
	});
	this.historyContainer.animate({scrollTop:this.historyContainer.get(0).scrollHeight}, 'slow');
};

assimilation.Play.prototype.updateBoard = function() {
	this.board.showState(this.game.state, this.players, this.game.size);
};

assimilation.Play.prototype.showHistoricState = function(moves) {
	var game = new assimilation.Game(this.game.state);
	var claims = game.getClaims(moves);
	this.board.showState({'c':claims}, this.players, this.game.size);
	this.showingHistoric = true;
};

assimilation.Play.prototype.updatePieces = function() {
	var me = this;
	this.piecesContainer.empty();
	var players = this['game']['state']['p'];
	for(var i=0; i<players.length; i++){
		if(typeof(players[i]['h']) != "number"){
			var player = players[i];
			var hand = player['h'];
			a.util.map(hand, function(tile){
				var color = me.players[player['i']].color;
				me.piecesContainer.append($('<div>').addClass('piece').addClass(color).text(getTileName(tile)).mouseover(function(){
					me.board.highlight(tile, color);
				}).mouseleave(function(){
					me.board.unhighlight(tile, color);
				}).click(function(){
					me.placeTile(tile);
				}));
				me.board.makeActive(tile,color, function(tile){
					me.placeTile(tile);
				});
			});
		}
	}
};

assimilation.Play.prototype.placeTile = function(tile) {
	var data = {
		'x':tile.x,
		'y':tile.y
	};
	var me = this;
	$.ajax('/assimilation/game/placetile/' + this.gameid, {
		'type':'POST',
		'data':data,
		'datatType':'json',
		'success':function(res){
			if(res['success']){
				me.update();
			}else if(res['error']){
				alert(res['error']);
			}
		},
		'error':function(res){

		}
	})
};