goog.provide('assimilation.JoinGameDialog');
goog.require('a.util');

assimilation.JoinGameDialog = function(){
	var me = this;
	this.id = null;
	this.pwrequired = false;
	this.container = $('.join-game');
	this.container.empty();
	this.cancel = $('<div>').addClass('cancel');
	this.title = $('<div>').addClass('title');
	this.pick = $('<div>').addClass('pick').text('Pick Your Color:');
	this.colorSelection = $('<div>').addClass('join-color-pick');
	var form = $('<form>');
	this.colorChoices = {};
	var colors = ['blue','green','yellow','orange','red','teal'];
	for(var i=0; i<colors.length; i++){
		var color = colors[i];
		form.append($('<input>').attr({
			'type':'radio',
			'name':'color',
			'value': color,
			'id':'join-'+color
		}));
		this.colorChoices[color]=$('<label>').addClass('color-choice').addClass(color).attr('for','join-'+color);
		form.append(this.colorChoices[color]);
	}
	this.colorSelection.append(form);
	this.password = $('<div>').addClass('enter-password').append($('<div>').addClass('pw-title').text('Password:'));
	this.passwordInput = $('<input>').attr('type','password');
	this.password.append(this.passwordInput);
	this.join = $('<div>').addClass('join-button').text('Join');


	this.container.append(this.cancel);
	this.container.append(this.title);
	this.container.append(this.pick);
	this.container.append(this.colorSelection);
	this.container.append(this.password);
	this.container.append(this.join);
	this.join.click(function(){
		me.joinGame();
	});
	this.cancel.click(function(){
		me.container.hide('fast');
		me.id = null;
	});
}

assimilation.JoinGameDialog.prototype.joinGame = function(){
	var id = this.id;
	var data = {
		'color':this.colorSelection.find(':checked').val()
	}
	if(this.pwrequired){
		data['password'] = this.passwordInput.val();
		console.log(data['password']);
	}
	$.ajax('/assimilation/game/join/' + id,{
		'data': data,
		'success': function(res){
			console.log(res);
			if(res['success']){
				window.location.pathname = "/assimilation/games";
			}
			else{
				if(res['error'])
					alert(res['error']);
			}
		},
		'error':function(res){
			console.log('error',res);
		},
		'type':'POST',
		'dataType':'json'
	});
}


assimilation.JoinGameDialog.prototype.show = function(id, name, color, password) {
	var me = this;
	this.id = id;
	this.pwrequired = password;
	this.container.hide('fast', function(){
		me.title.text("Join " + name + "'s Game!");
		for(key in me.colorChoices){
			if(key == color){
				me.colorChoices[color].attr('for','join-'+color+'-no').addClass('off-limits');
				me.colorSelection.find('input').filter('#join-'+color).attr('checked',false);
			}
			else{
				me.colorChoices[key].attr('for','join-'+key).removeClass('off-limits');
			}
		}
		if(password){
			me.password.show();
			me.join.addClass('pw');
		}
		else{
			me.password.hide();
			me.join.removeClass('pw');
		}
		me.container.show('fast');
	});
};