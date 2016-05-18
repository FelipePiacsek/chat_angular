angular.module('chatApp').controller('MessageTabController', function(ChatService, CallbackUtils, HTTPService) {
	
	var callbackMessages = function(messages) {
		$scope.messages = messages.messages;
	};
	
	var initController = function() {
		ChatService.registerLoadMessagesFunction(callBackMessages);
	};
	initController();



});