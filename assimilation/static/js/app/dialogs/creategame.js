goog.provide('assimilation.CreateGameDialog');
goog.require('goog.array');


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

/**
* @constructor
*/
assimilation.CreateGameDialog = function(){
	this.sizes = ['8','10','12'];
	this.colors = ['blue','green','yellow','orange','red','teal'];
	this.container = $('.game-create');
	this.title = this.createTitle();
	this.sizeOptions = this.createSizeOptions();
	this.colorOptions = this.createColorOptions();
	this.passwordOption = this.createPasswordOption();
	this.button = this.createButton();

	this.container.append(this.title);
	this.container.append(this.sizeOptions);
	this.container.append(this.colorOptions);
	this.container.append(this.passwordOption);
	this.container.append(this.button);

	var me = this;

	this.button.click(function(){
		me.makeGame();
	});
};

assimilation.CreateGameDialog.prototype.makeGame = function() {
	var size = this.sizeOptions.find(':checked').val();
	var color = this.colorOptions.find(':checked').val();
	var usePassword = this.passwordOption.find('input[type=checkbox]').is(':checked');
	var password = this.passwordOption.find('#game-password').val();
	var again = this.passwordOption.find('#game-pass-again').val();
	var data = {
		"size":size,
		"color":color,
	};

	if(usePassword){
		if(password != again){
			alert("Passwords must match!");
			return;
		}
		if(password.length == 0){
			alert("Minimum password length is 1");
			return;
		}
		data["password"] = password;
	}

	$.ajax('/assimilation/game/create',{
		'type':'POST',
		'data':data,
		'dataType':'json',
		'success':function(response){
			console.log(response);
			// window.location.pathname = "/assimilation/games";
		}
	});
};

assimilation.CreateGameDialog.prototype.createTitle = function() {
	var result = $('<div>');
	result.addClass('game-create-title').text('Create A Game');
	return result;
};

assimilation.CreateGameDialog.prototype.createSizeOptions = function() {
	var result = $('<div>');
	result.addClass('game-create-size');
	$('<span>').addClass('game-create-size-title').text('Size of Board').appendTo(result);
	var options = $('<div>').addClass('game-create-size-options');
	var form = $('<form>');
	goog.array.forEach(this.sizes, function(size,i){
		var input = $('<input>').attr({'type':'radio','name':'size','id':'size-'+size, 'value':size, 'checked':i==1});
		var label = $('<label>').attr('for','size-'+size).append($('<a>').text(size+'x'+size));
		form.append(input);
		form.append(label);
		form.append($('<br>'));
	});
	options.append(form);
	result.append(options);
	return result;
};

assimilation.CreateGameDialog.prototype.createColorOptions = function() {
	var result = $('<div>');
	result.addClass('game-create-color').text('Your Color').append($('<br>'));
	var colors = $('<div>').addClass('colors');
	var form = $('<form>');
	goog.array.forEach(this.colors, function(color,i){
		var input = $('<input>').attr({'type':'radio','name':'color','id':color, 'value':color, 'checked':i==0});
		var label = $('<label>').attr('for',color).addClass('color-choice').addClass(color);
		form.append(input);
		form.append(label);
	});
	colors.append(form);
	result.append(colors);
	return result;
};

assimilation.CreateGameDialog.prototype.createPasswordOption = function() {
	var result = $('<div>');
	result.addClass('game-create-password');

	var title = $('<div>').addClass('game-create-password-title').text('Require Password?');
	title.append($('<input>').attr({'id':'use-password','type':'checkbox'}));

	var form = $('<form>');

	var input = $('<input>').attr({'type':'password','id':'game-password'});
	var label = $('<span>').text('Password:');
	form.append(label);
	form.append(input);
	
	input = $('<input>').attr({'type':'password','id':'game-pass-again'});
	label = $('<span>').text('Again:');
	form.append(label);
	form.append(input);

	result.append(title);
	result.append(form);
	return result;
};

assimilation.CreateGameDialog.prototype.createButton = function() {
	var result = $('<div>').addClass('game-create-button').text('Create Game');
	return result;
};