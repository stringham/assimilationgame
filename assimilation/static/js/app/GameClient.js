goog.provide('assimilation.GameClient');
goog.require('assimilation.Play');
goog.require('assimilation.Chats');
goog.require('assimilation.SwapTileDialog');
goog.require('assimilation.Board');

/**
* @constructor
*/
assimilation.GameClient = function(gameid){
	this.gameid = gameid;
	this.play = new assimilation.Play(gameid);
}

goog.exportSymbol('assimilation.GameClient', assimilation.GameClient);
