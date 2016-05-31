'use strict';
angular.module('chatApp').service('ChatService',  function(UserData, HTTPService, CallbackUtils, ConversationsSocket, ChatMessageFactory, SocketMessageFactory){

	var currentConversationId = null;

	var messagesReceivedCallback = {};

	var newMessageCallback = {};

	var conversationsReceivedCallback = {};

	var conversations = {};

	var socketCallback = function(message) {
		console.log("Socket callback!");
		var id = UserData.getId();
        var content = angular.fromJson(message.data);
        content.ts = new Date(content.ts);
        console.log(content);
    	for(var i = 0; i < newMessageCallback[id].length; i++){
    		newMessageCallback[id][i](content);
    	}
    	if(conversations[content.conversation_id]){
    		conversations[content.conversation_id].messages.push(content);
    	}
    };

    this.startChatSession = function(){
    	ConversationsSocket.connect(socketCallback);
    };
    this.startChatSession();

	var loadMessages = function(conversation){
		var id = UserData.getId();
		var endpoint = "/conversations/" + currentConversationId + "/messages/";
	    HTTPService.requests(endpoint).get().$promise.then(function(response) {
	    	for(var i = 0; i < messagesReceivedCallback[id].length; i++){
	    		messagesReceivedCallback[id][i](response);
	    	}
	    	conversations[currentConversationId] = {};
	    	conversations[currentConversationId].metadata = {};
	    	conversations[currentConversationId].metadata.type = conversation.type;
	    	conversations[currentConversationId].messages = response.messages;
	    }, function(promise) {
	        CallbackUtils.mostrarErros(promise);
	    });
	};

	this.loadConversationsList = function(){
		var id = UserData.getId();
		var endpoint = "conversations/";
	    HTTPService.requests(endpoint).get().$promise.then(function(response) {
	    	console.log(response);
			for(var i = 0; i < conversationsReceivedCallback[id].length; i++){
	    		conversationsReceivedCallback[id][i](response);
	    	}
	    }, function(promise) {
	        CallbackUtils.mostrarErros(promise);
	    });
	};

	this.setCurrentConversationId = function (conversation){
		var id = UserData.getId();
		currentConversationId = conversation.id;
		if(!conversations[currentConversationId]){
			loadMessages(conversation);
		}else{
			for(var i = 0; i < messagesReceivedCallback[id].length; i++){
	    		messagesReceivedCallback[id][i](conversations[currentConversationId]);
	    	}
		}
	};

	this.addMessagesReceivedCallback = function (callback){
		var id = UserData.getId();
		if(!messagesReceivedCallback[id]){
			messagesReceivedCallback[id] = [];
		}
		messagesReceivedCallback[id].push(callback);
	};

	this.addNewMessageCallback = function (callback){
		var id = UserData.getId();
		if(!newMessageCallback[id]){
			newMessageCallback[id] = [];
		}
		newMessageCallback[id].push(callback);
	};

	this.addConversationsReceivedCallback = function (callback){
		var id = UserData.getId();
		if(!conversationsReceivedCallback[id]){
			conversationsReceivedCallback[id] = [];
		}		
		conversationsReceivedCallback[id].push(callback);
		this.loadConversationsList();
	};

	this.sendTextMessage = function(text){
		console.log("User " + UserData.getId() + " is sending a message: " + text);
		var chatMessage = ChatMessageFactory.buildTextMessage(text, currentConversationId);
		var socketMessage = SocketMessageFactory.buildMessage("chat_message", chatMessage);
		ConversationsSocket.send(socketMessage);
	};

	this.getCurrentConversationId = function(){
		return currentConversationId;
	};

	this.markAsRead = function(message){
		console.log("Marking as read...");
		var socketMessage = SocketMessageFactory.buildMessage("mark_as_read", message);
		console.log(socketMessage);
		ConversationsSocket.send(socketMessage);	
	};

	this.destroy = function(){
		console.log("Destroying chat for user " + UserData.getId() + ".");
		ConversationsSocket.disconnect();
		currentConversationId = null;
		messagesReceivedCallback = {};
		newMessageCallback = {};
		conversationsReceivedCallback = {};
		conversations = {};
	};

});