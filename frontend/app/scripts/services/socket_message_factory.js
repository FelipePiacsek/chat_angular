'use strict';
angular.module('chatApp').service('SocketMessageFactory',  function(){

	this.buildMessage = function(type, data){
		var message = {};
		message.type = type;
		message.data = data;
		return message;
	};

});