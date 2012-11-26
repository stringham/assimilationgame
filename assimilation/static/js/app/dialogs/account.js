goog.provide('assimilation.AccountDialog');

/**
* @constructor
*/
assimilation.AccountDialog = function(){
	var me = this;
	this.summaryContainer = $('.account');
	this.updateContainer = $('.update-account');

	this.nameInput = this.updateContainer.find('.name').find('input');
	this.emailInput = this.updateContainer.find('.email').find('input');
	this.passwordInput = this.updateContainer.find('.password').find('input');
	this.newPassInput = this.updateContainer.find('.new-password').find('input');
	this.newPassAgainInput = this.updateContainer.find('.repeat-password').find('input');


	this.openButton = $('.account-open');
	this.closeButton = this.summaryContainer.find('.account-close');
	this.updateButton = this.summaryContainer.find('.account-update');
	this.signoutButton = this.summaryContainer.find('.account-signout');

	this.saveButton = this.updateContainer.find('.save');
	this.cancelButton = this.updateContainer.find('.cancel');

	this.closeButton.click(function(){
		me.updateContainer.hide(450);
		me.summaryContainer.hide(450);
	});

	this.openButton.click(function(){
		me.summaryContainer.stop().toggle(450);
	});

	this.updateButton.click(function(){
		me.updateContainer.toggle(450);
	});

	this.cancelButton.click(function(){
		me.updateContainer.hide(450);
	});

	this.saveButton.click(function(){
		me.saveAccount();
	});

	this.signoutButton.click(function(){
		window.location.pathname = '/assimilation/auth/logout';
	});
};

assimilation.AccountDialog.prototype.saveAccount = function() {
	var me = this;
	var data = {
		'name':this.nameInput.val(),
		'email':this.emailInput.val(),
		'password':this.passwordInput.val(),
		'new-password':this.newPassInput.val(),
		'new-pass-again':this.newPassAgainInput.val()
	};

	$.ajax('/assimilation/auth/update/', {
		'type':'POST',
		'dataType':'json',
		'data':data,
		'success': function(res){
			if(res['success']){
				me.updateContainer.hide(450, function(){
					window.location.reload();
				});
			} else{
				if(res['error'])
					alert(res['error']);
			}
		},
		'error': function(res){

		}
	});
};


goog.exportSymbol('assimilation.AccountDialog', assimilation.AccountDialog);
