'use strict';
angular.module('chatApp').service('SocketMessageFactory',  function(){

	var messageSending = function(data){
		return data;
	};

	var markingAsRead = function(message){
		var data = {};
		data.conversation_id = message.conversation_id
		return data;
	};

	var dataRetriever;
	var initService = function(){
		dataRetriever = {};
		dataRetriever['mark_as_read'] = markingAsRead;
		dataRetriever['chat_message'] = messageSending;
	};
	initService();

	this.buildMessage = function(type, data){
		var message = {};
		message.type = type;
		message.data = dataRetriever[type](data);
		return message;
	};

});