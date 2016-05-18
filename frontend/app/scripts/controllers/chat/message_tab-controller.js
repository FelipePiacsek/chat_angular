'use strict';
angular.module('chatApp').controller('MessageTabController', function(ChatService, $scope) {
	
	var callbackMessages = function(messages) {
		$scope.messages = messages.messages;
	};
	
	var initController = function() {
		ChatService.registerLoadMessagesFunction(callBackMessages);
	};
	initController();



});