angular.module('chatApp').service('ChatService',  function(HTTPService, CallbackUtils){

	var currentConversationId = null;

	var messagesReceivedCallback = null;

	this.setCurrentConversationId = function (id){
		currentConversationId = id;
	};

	this.setMessagesReceivedCallback = function (callback){
		messagesReceivedCallback = callback;
	};

	var loadMessages = function(){
		var endpoint = "/conversations/" + currentConversationId + "/";
	    HTTPService.requests(endpoint).get().$promise.then(function(response) {
	    	messagesReceivedCallback(response)
	    }, function(promise) {
	        CallbackUtils.mostrarErros(promise);
	    });
	};

});