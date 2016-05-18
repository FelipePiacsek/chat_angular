angular.module('chatApp').controller('ConversationsListController', function(ChatService) {
	
	var callbackConversations = function(covnersations) {
		$scope.covnersations = covnersations.covnersations;
	};

	var initController = function() {
		ChatService.setConversationsReceivedCallback(callbackConversations);
	};
	initController();



});