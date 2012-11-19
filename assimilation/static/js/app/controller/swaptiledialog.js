goog.provide('assimilation.SwapTileDialog');
goog.require('a.util');

assimilation.SwapTileDialog = function(){
	var me = this;
	this.id = null;
	this.pwrequired = false;
	this.container = $('.swap-tiles');
	this.cancel = this.container.find('.cancel');
	this.pick = this.container.find('.pick');
	this.tileSelection = this.container.find('.swap-tile-pick');
	this.button = this.container.find('.swap-button');
	this.tiles = [];
	this.button.click(function(){
		me.exchange();
	});
	this.cancel.click(function(){
		me.container.hide('fast');
		me.id = null;
	});
}

assimilation.SwapTileDialog.prototype.exchange = function(){
	var checked = this.container.find(':checked');
	var me = this;
	var tilesToSwap = [];
	a.util.map(checked, function(tile){tilesToSwap.push(me.tiles[tile.value]);})
	var data = {
		'swap':JSON.stringify(tilesToSwap)
	};

	$.ajax('/assimilation/game/swap/' + this.id, {
		'type':'POST',
		'data':data,
		'dataType':'json',
		'success':function(res){
			if(res['success']){
				me.container.hide('fast');
			} else if(res['error']){
				alert(res['error']);
			}
		},
		'error':function(res){
			console.log('error',res);
		}
	});
}


assimilation.SwapTileDialog.prototype.show = function(id, tiles, color) {
	var me = this;
	this.id = id;
	this.tiles = tiles;
	this.tileSelection.empty();
	a.util.map(tiles, function(tile,i){
		var input = $('<input>').attr({
			'type':'checkbox',
			'name':'tile',
			'id':'tile-' + (i),
			'value': i
		});
		var label = $('<label>').attr({
			'for':'tile-' + (i),
		}).addClass('color-choice').addClass(color).text(String.fromCharCode(65 + tile.x) + (tile.y+1));
		me.tileSelection.append(input).append(label);
	});
	this.container.show('fast');
};