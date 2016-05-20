'use strict';
angular.module('chatApp').controller('ConversationsInputController', function(ChatService, $scope) {

	$scope.sendMessage = function(){
		var message = {};
		message.message = $scope.message;
		ChatService.sendMessage(message);
	};

});