'use strict';
angular.module('chatApp').service('ChatService',  function(HTTPService, CallbackUtils, ConversationsSocket, MessageFactory){

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

	this.createUser = function(){
		var endpoint = "/create_user/";
		var user = {};
		user.username="felruivo";
		user.password="felipe";
		user.first_name="Felipe";
		user.last_name="Piacsek";
		user.picture="https://uploads.socialspirit.com.br/fanfics/capitulos/fanfiction-originais-bambam-enlouquecendo-no-treino-com-felipe-franco-5293873-070320161619.jpg";
		user.email="felipe.piacsek@gmail.com";
		console.log(user);
	    HTTPService.requests(endpoint).post(user).$promise.then(function(response) {
	    	console.log("Ok.");
	    }, function(promise) {
	        CallbackUtils.mostrarErros(promise);
	    });
	}

});