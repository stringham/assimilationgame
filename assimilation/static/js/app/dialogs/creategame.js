goog.provide('assimilation.CreateGameDialog');
goog.require('goog.array');
goog.require('goog.dom');
goog.require('goog.dom.query');
goog.require('goog.events');

/**
* @constructor
*/
assimilation.CreateGameDialog = function(){
	this.sizes = ['8','10','12'];
	this.colors = ['blue','green','yellow','orange','red','teal'];
	this.container = goog.dom.getElementByClass('game-create');
	this.title = this.createTitle();
	this.sizeOptions = this.createSizeOptions();
	this.colorOptions = this.createColorOptions();
	this.passwordOption = this.createPasswordOption();
	this.button = this.createButton();
	goog.dom.appendChild(this.container, this.title);
	goog.dom.appendChild(this.container, this.sizeOptions);
	goog.dom.appendChild(this.container, this.colorOptions);
	goog.dom.appendChild(this.container, this.passwordOption);
	goog.dom.appendChild(this.container, this.button);

	var me = this;

	goog.events.listen(this.button, 'click', function(){
		me.createGame();
	});
}

assimilation.CreateGameDialog.prototype.createGame = function(){
	var size = goog.dom.query('input:checked', this.sizeOptions)[0].value;
	var color = goog.dom.query('input:checked', this.colorOptions)[0].value;
	var usePassword = goog.dom.query('input[type=checkbox]')[0].checked;
	if(usePassword){
		var password = goog.dom.query('#game-password')[0].value;
		var again = goog.dom.query('#game-pass-again')[0].value;
		if(password.length == 0){
			alert('Either enter a password or uncheck the password option!');
			return;
		}
		if(password != again){
			alert('Passwords do not match!');
			return;
		}
	}
	alert('creating new game with size ' + size + ' you are ' + color + ' and are ' + (usePassword ?  '' : 'not ') + 'using a password');
}

assimilation.CreateGameDialog.prototype.createTitle = function() {
	var result = goog.dom.createDom('div', {'class':'game-create-title'}, 'Create A Game');
	return result;
};

assimilation.CreateGameDialog.prototype.createSizeOptions = function() {
	var result = goog.dom.createDom('div', {'class':'game-create-size'});
	goog.dom.appendChild(result, goog.dom.createDom('span',{'class':'game-create-size-title'}, 'Size of Board'));
	var options = goog.dom.createDom('div', {'class':'game-create-size-options'});
	var form = goog.dom.createDom('form');
	goog.array.forEach(this.sizes, function(size,i){
		var input = goog.dom.createDom('input',{'type':'radio','name':'size','id':'size-'+size, 'value':size, 'checked':i==1});
		var label = goog.dom.createDom('label',{'for':'size-'+size});
		var a = goog.dom.createDom('a',{},size+'x'+size);
		goog.dom.appendChild(form, input);
		goog.dom.appendChild(label,a);
		goog.dom.appendChild(form,label);
		goog.dom.appendChild(form, goog.dom.createDom('br'));
	});
	goog.dom.appendChild(options, form);
	goog.dom.appendChild(result, options);
	return result;
};

assimilation.CreateGameDialog.prototype.createColorOptions = function() {
	var result = goog.dom.createDom('div', {'class':'game-create-color'}, 'Your Color');
	goog.dom.appendChild(result, goog.dom.createDom('br'));
	var colors = goog.dom.createDom('div', {'class':'colors'});
	var form = goog.dom.createDom('form');
	var select = Math.floor(this.colors.length*Math.random());
	goog.array.forEach(this.colors, function(color,i){
		var input = goog.dom.createDom('input',{'type':'radio','name':'color','id':color, 'value':color, 'checked':i==select});
		var label = goog.dom.createDom('label',{'for':color, 'class': 'color-choice ' + color});
		goog.dom.appendChild(form, input);
		goog.dom.appendChild(form,label);
	});
	goog.dom.appendChild(colors, form);
	goog.dom.appendChild(result, colors);
	return result;
};

assimilation.CreateGameDialog.prototype.createPasswordOption = function() {
	var result = goog.dom.createDom('div', {'class':'game-create-password'});
	var title = goog.dom.createDom('div',{'class':'game-create-password-title'}, 'Require Password?');
	var check = goog.dom.createDom('input',{'type':'checkbox', 'id':'use-password'});

	var form = goog.dom.createDom('form');
	var input = goog.dom.createDom('input',{'type':'password','id':'game-password'});
	var label = goog.dom.createDom('span',{},'Password:');
	goog.dom.appendChild(form,label);
	goog.dom.appendChild(form, input);
	input = goog.dom.createDom('input',{'type':'password','id':'game-pass-again'});
	label = goog.dom.createDom('span',{},'Again:');
	goog.dom.appendChild(form,label);
	goog.dom.appendChild(form, input);


	goog.dom.appendChild(title, check);
	goog.dom.appendChild(result, title);
	goog.dom.appendChild(result, form);
	return result;
};

assimilation.CreateGameDialog.prototype.createButton = function() {
	var result = goog.dom.createDom('div', {'class':'game-create-button'}, 'Create Game');
	return result;
};


// goog.provide('assimilation.CreateGameDialog');
// goog.require('goog.array');

// /**
// * @constructor
// */
// assimilation.CreateGameDialog = function(){
// 	this.sizes = ['8','10','12'];
// 	this.colors = ['blue','green','yellow','orange','red','teal'];
// 	this.container = $('.game-create');
// 	this.title = this.createTitle();
// 	this.sizeOptions = this.createSizeOptions();
// 	this.colorOptions = this.createColorOptions();
// 	this.passwordOption = this.createPasswordOption();
// 	this.button = this.createButton();

// 	this.container.append(this.title);
// 	this.container.append(this.sizeOptions);
// 	this.container.append(this.colorOptions);
// 	this.container.append(this.passwordOption);
// 	this.container.append(this.button);
// }

// assimilation.CreateGameDialog.prototype.createTitle = function() {
// 	var result = $('<div>');
// 	result.addClass('game-create-title').text('Create A Game');
// 	return result;
// };

// assimilation.CreateGameDialog.prototype.createSizeOptions = function() {
// 	var result = $('<div>');
// 	result.addClass('game-create-size');
// 	$('<span>').addClass('game-create-size-title').text('Size of Board').appendTo(result);
// 	var options = $('<div>').addClass('game-create-size-options');
// 	var form = $('<form>');
// 	goog.array.forEach(this.sizes, function(size,i){
// 		var input = $('<input>').attr({'type':'radio','name':'size','id':'size-'+size, 'value':size, 'checked':i==1});
// 		var label = $('<label>').attr('for','size-'+size).append($('<a>').text(size+'x'+size));
// 		form.append(input);
// 		form.append(label);
// 		form.append($('<br>'));
// 	});
// 	options.append(form);
// 	result.append(options);
// 	return result;
// };

// assimilation.CreateGameDialog.prototype.createColorOptions = function() {
// 	var result = $('<div>');
// 	result.addClass('game-create-color').text('Your Color').append($('<br>'));
// 	var colors = $('<div>').addClass('colors');
// 	var form = $('<form>');
// 	goog.array.forEach(this.colors, function(color,i){
// 		var input = $('<input>').attr({'type':'radio','name':'color','id':color, 'value':color, 'checked':i==0});
// 		var label = $('<label>').attr('for',color).addClass('color-choice').addClass(color);
// 		form.append(input);
// 		form.append(label);
// 	});
// 	colors.append(form);
// 	result.append(colors);
// 	return result;
// };

// assimilation.CreateGameDialog.prototype.createPasswordOption = function() {
// 	var result = $('<div>');
// 	result.addClass('game-create-password');

// 	var title = $('<div>').addClass('game-create-password-title').text('Require Password?');
// 	title.append($('<input>').attr({'id':'game-password','type':'checkbox'}));

// 	var form = $('<form>');

// 	var input = $('<input>').attr({'type':'password','id':'game-password'});
// 	var label = $('<span>').text('Password:');
// 	form.append(label);
// 	form.append(input);
	
// 	input = $('<input>').attr({'type':'password','id':'game-pass-again'});
// 	label = $('<span>').text('Again:');
// 	form.append(label);
// 	form.append(input);

// 	result.append(title);
// 	result.append(form);
// 	return result;
// };

// assimilation.CreateGameDialog.prototype.createButton = function() {
// 	var result = $('<div>').addClass('game-create-button').text('Create Game');
// 	return result;
// };