'use strict';
angular.module('chatApp').controller('ConversationsListController', function(ChatService, $scope) {
	
	var callbackConversations = function(conversations) {
		$scope.conversations = conversations.conversations;
	};

	var initController = function() {
		ChatService.setConversationsReceivedCallback(callbackConversations);
		$scope.feliz = "Feliz."
	};
	initController();



});