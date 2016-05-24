'use strict';
angular.module('chatApp').service('ChatService',  function(HTTPService, CallbackUtils, ChatSocket, MessageFactory){

	var currentConversationId = null;

	var messagesReceivedCallback = null;

	var newMessageCallback = null;

	var conversationsReceivedCallback = null;

	var conversations = {};

	ChatSocket.onMessage(function(message) {
        console.log(message);
    });

	var loadMessages = function(conversation){
		var endpoint = "/conversations/" + currentConversationId + "/messages/";
	    HTTPService.requests(endpoint).get().$promise.then(function(response) {
	    	messagesReceivedCallback(response)
	    	conversations[currentConversationId] = {};
	    	conversations[currentConversationId].metadata = {};
	    	conversations[currentConversationId].metadata.type = conversation.type;
	    	conversations[currentConversationId].messages = [];
	    }, function(promise) {
	        CallbackUtils.mostrarErros(promise);
	    });
	};

	var loadConversationsList = function(){
		var endpoint = "conversations/";
	    HTTPService.requests(endpoint).get().$promise.then(function(response) {
	    	conversationsReceivedCallback(response)
	    }, function(promise) {
	        CallbackUtils.mostrarErros(promise);
	    });
	};

	this.setCurrentConversationId = function (conversation){
		currentConversationId = conversation.id;
		if(!conversations[currentConversationId]){
			loadMessages(conversation);
		}else{
			messagesReceivedCallback(conversations[currentConversationId].messages);
		}
	};

	this.setMessagesReceivedCallback = function (callback){
		messagesReceivedCallback = callback;
	};

	this.setConversationsReceivedCallback = function (callback){
		conversationsReceivedCallback = callback;
		loadConversationsList();
	};

	this.sendTextMessage = function(text){
		var message = MessageFactory.buildTextMessage(text, currentConversationId);
		console.log(message);
		ChatSocket.send(message);
	};

});