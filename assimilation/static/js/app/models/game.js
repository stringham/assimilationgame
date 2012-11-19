goog.provide('assimilation.Game');
goog.require('a.util');
/**
* @constructor
*/
assimilation.Game = function(state){
	this.state = state;
}

assimilation.Game.prototype.getClaims = function(moves) {
	var board = [];
	var me=this;
	var claims = [];
	for(var i=0; i<this.state['he']; i++){
		board.push([]);
		for(var j=0; j<this.state['w']; j++){
			board[i].push(null);
		}
	}
	var history = this.state['h'];
	for(var i=0; i<moves; i++){
		placeTile(history[i].t, history[i].o);
	}

	return claims;
	
	function setOwner(tile, player){
		board[tile.x][tile.y] = player;
		for(var i=0; i<claims.length; i++){
			if(claims[i].t.x == tile.x && claims[i].t.y == tile.y){
				claims[i].o = player
				return;
			}
		}
		claims.push({'t':tile, 'o':player});
	}

	function getOwner(tile){
		if(tile.x < 0 || tile.y < 0 || tile.x >= me.state['w'] || tile.y >= me.state['he'])
			return null;
		return board[tile.x][tile.y];
	}

	function contains(array, tile){
		for(var i=0; i<array.length; i++){
			if(array[i].x == tile.x && array[i].y == tile.y)
				return true;
		}
		return false;
	}

	function getNeighbors(tile, tiles){
		if(getOwner(tile) == null || contains(tiles,tile))
			return;
		tiles.push(tile);
		getNeighbors({x:tile.x-1,y:tile.y},tiles);
		getNeighbors({x:tile.x+1,y:tile.y},tiles);
		getNeighbors({x:tile.x,y:tile.y+1},tiles);
		getNeighbors({x:tile.x,y:tile.y-1},tiles);
	}

	function placeTile(tile, player){
		if(tile.x == -1 || tile.y == -1)
			return;
		setOwner(tile,player);
		var neighbors = [];
		getNeighbors(tile, neighbors);
		var armies = {};

		a.util.map(neighbors, function(tile){
			if(!armies[getOwner(tile)])
				armies[getOwner(tile)] = 0;
			armies[getOwner(tile)]++;
		});
		var largest = armies[player];
		var owner = player;
		for(var id in armies){
			if(armies[id] > largest){
				largest = armies[id];
				owner = id;
			} else if(armies[id] == largest){
				owner = player;
			}
		}

		a.util.map(neighbors, function(tile){
			setOwner(tile, owner);
		});
	}

};