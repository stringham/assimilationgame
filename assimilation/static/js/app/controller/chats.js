goog.provide('assimilation.Chats');
goog.require('goog.string');

function getCookie(name)
{
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?

            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$.ajaxSetup({ 
     beforeSend: function(xhr, settings) {
         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             // Only send the token to relative URLs i.e. locally.
             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         }
     } 
});

assimilation.Chats = function(gameId){
	this.gameId = gameId;
	this.container = $('.messages');
	this.container.empty();
	this.messages = [];
	this.last_message = 0;
	var me = this;
	this.submitButton = $('.send-button');
	this.input = $('.text-input > input');
	this.input.keypress(function (e) {
		if (e.which == 13) {
			me.sendMessage();
		}
	});
	this.submitButton.click(function(){
		me.sendMessage();
	});
	
	me.update();
}
		
		

assimilation.Chats.prototype.appendMessage = function(name, message, color) {
	// <div class='name blue'>Kevin</div>
	// <div class='message'>Nice Move!</div>
	var user = $('<div>').addClass('name ' + color).text(goog.string.unescapeEntities(name));
	var content = $('<div>').addClass('message').text(goog.string.unescapeEntities(message).split(/([^\s-]{15})([^\s-]{15})/).join('\u200B'));
	this.container.append(user).append(content);
};

assimilation.Chats.prototype.update = function() {
	var me = this;

	$.ajax('/assimilation/chats/' + this.gameId,{
		'success': function(data){
			if(data['success']){
				me.update();
				return;
			}
			me.last_message = data['latest'];
			for(var i=0; i<data.messages.length; i++){
				user = data.users[data.messages[i].userid];
				if(user)
					var color = user.color;
				else
					var color = 'black';

				me.appendMessage(data.messages[i].name, data.messages[i].text, color);
			}
			if(data.messages.length > 0)
				me.container.animate({scrollTop:me.container.get(0).scrollHeight}, 'fast');
			setTimeout(function() {
				me.update();
			}, 500);
		},
		'error': function(data){
			console.log('error',data);
		},
		'dataType':'json',
		'data':{
			'last_message':this.last_message
		}
	});
};

assimilation.Chats.prototype.sendMessage = function() {
	var me = this;
	var message = this.input.val();
	this.input.val('');
	if(message.length == 0)
		return;

	var data = {
		'content': message
	};

	$.ajax('/assimilation/chats/' + this.gameId, {
		'type':'POST',
		'success': function(data){
		},
		'error': function(){

		},
		'data':data
	});
};