goog.provide('assimilation.Board');

/**
* @constructor
*/
assimilation.Board = function(){
	this.container = $('.game-board');
	// this.container.empty();
	this.numbers = $('.numbers');
	this.letters = $('.letters')
	// this.setSize(10,10);
}

assimilation.Board.prototype.setSize = function(width, height) {
	this.container.empty();
	this.board = [];
	for(var i=0; i<height; i++){
		this.board.push([]);
		var row = $('<div>').addClass('game-row');
		for(var j=0; j<width; j++){
			var cell = $('<div>').addClass('game-cell');
			row.append(cell)
			this.board[i].push(cell);
		}
		this.container.append(row);
	}

	this.numbers.empty();
	this.letters.empty();
	var numbers = $('<table>')
	var tr = $('<tr>');
	for(var i=0; i<width; i++){
		tr.append($('<td>').text(''+(i+1)));
	}
	numbers.append(tr);
	this.numbers.append(numbers);

	var letters = $('<table>');
	for(var i=0; i<height; i++){
		tr = $('<tr>');
		tr.append($('<td>').text(String.fromCharCode(i+65)));
		letters.append(tr);
	}
	this.letters.append(letters);
};

assimilation.Board.prototype.showState = function(state, players, size) {
	var claim, color, tile;
	this.setSize(size, size);
	if(state['c']){
		for(var i=0; i< state['c'].length; i++){
			claim = state['c'][i];
			tile = claim['t'];
			color = players[claim['o']].color;
			this.board[tile['x']][tile['y']].addClass(color);
		}
		if(state['p']){
			for(var i=0; i<state['p'].length; i++){
				if(typeof(state['p'][i]['h']) != "number"){
					for(var j=0; j<state['p'][i]['h'].length; j++){
						tile = state['p'][i]['h'][j];
						this.board[tile['x']][tile['y']].addClass('gray');
					}
				}
			}
		}
	}
};

assimilation.Board.prototype.makeActive = function(tile, color, onclick){
	var me = this;
	this.board[tile.x][tile.y].mouseover(function(dom){
		me.board[tile.x][tile.y].addClass(color).addClass('active');
	}).mouseout(function(dom){
		me.board[tile.x][tile.y].removeClass(color).removeClass('active');
	}).click(function(){
		onclick(tile);
	});
}

assimilation.Board.prototype.highlight = function(tile, color) {
	this.board[tile.x][tile.y].addClass(color);
};

assimilation.Board.prototype.unhighlight = function(tile, color) {
	this.board[tile.x][tile.y].removeClass(color);
	// body...
};