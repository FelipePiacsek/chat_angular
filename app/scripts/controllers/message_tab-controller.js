angular.module('chat').controller('MessageTabController', function(ChatService, CallbackUtils, HTTPService) {
	
	$scope.init = function() {
		ChatService.registerLoadMessagesFunction(callBackMessages);
	}

	var callbackMessages = function(messages) {
		$scope.messages = messages.messages;
	}


});