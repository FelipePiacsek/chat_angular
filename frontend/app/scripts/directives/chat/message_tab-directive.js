'use strict';
angular.module('chatApp').directive('messagesTab', ['ChatService', function(ChatService) {

	return {
		restrict: 'E',
		templateUrl: 'views/chat/messages-tab.html',
		link: function(scope, element, attrs){
			var callbackMessages = function(messages) {
				scope.messages = messages.messages;
			};
			
			var initController = function() {
				ChatService.setMessagesReceivedCallback(callbackMessages);
			};
			initController();		
		}
	};


}]);