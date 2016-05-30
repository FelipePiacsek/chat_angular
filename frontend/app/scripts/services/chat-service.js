'use strict';
angular.module('chatApp').service('ChatService',  function(UserData, HTTPService, CallbackUtils, ConversationsSocket, MessageFactory){

	var currentConversationId = null;

	var messagesReceivedCallback = [];

	var newMessageCallback = [];

	var conversationsReceivedCallback = [];

	var conversations = {};

	ConversationsSocket.onMessage(function(message) {
        console.log(message);
    	for(var i = 0; i < newMessageCallback.length; i++){
    		newMessageCallback[i](response);
    	}
    });

	var loadMessages = function(conversation){
		var endpoint = "/conversations/" + currentConversationId + "/messages/";
	    HTTPService.requests(endpoint).get().$promise.then(function(response) {
	    	for(var i = 0; i < messagesReceivedCallback.length; i++){
	    		messagesReceivedCallback[i](response);
	    	}
	    	conversations[currentConversationId] = {};
	    	conversations[currentConversationId].metadata = {};
	    	conversations[currentConversationId].metadata.type = conversation.type;
	    	conversations[currentConversationId].messages = response.messages;
	    }, function(promise) {
	        CallbackUtils.mostrarErros(promise);
	    });
	};

	var loadConversationsList = function(){
		var endpoint = "conversations/";
	    HTTPService.requests(endpoint).get().$promise.then(function(response) {
	    	console.log(response);
			for(var i = 0; i < conversationsReceivedCallback.length; i++){
	    		conversationsReceivedCallback[i](response);
	    	}
	    }, function(promise) {
	        CallbackUtils.mostrarErros(promise);
	    });
	};

	this.setCurrentConversationId = function (conversation){
		currentConversationId = conversation.id;
		if(!conversations[currentConversationId]){
			loadMessages(conversation);
		}else{
			for(var i = 0; i < messagesReceivedCallback.length; i++){
	    		messagesReceivedCallback[i](conversations[currentConversationId]);
	    	}
		}
	};

	this.addMessagesReceivedCallback = function (callback){
		messagesReceivedCallback.push(callback);
	};

	this.addNewMessageCallback = function (callback){
		newMessageCallback.push(callback);
	};

	this.addConversationsReceivedCallback = function (callback){
		conversationsReceivedCallback.push(callback);
		loadConversationsList();
	};

	this.sendTextMessage = function(text){
		var message = MessageFactory.buildTextMessage(text, currentConversationId);
		console.log(message);
		ConversationsSocket.send(message);
	};

});