'use strict';
angular.module('chatApp').directive('conversationsTab', ['ChatService', function(ChatService) {

	return {
		restrict: 'E',
		templateUrl: 'views/chat/conversations-tab.html',
		link: function(scope, element, attrs){
			var callbackConversations = function(conversations) {
				scope.conversations = conversations.conversations;
				for (var i = 0; i < scope.conversations.length; i++){
					scope.conversations[i].last_message.date = new Date(scope.conversations[i].last_message.date);
				}
				scope.selectConversation(scope.conversations[0]);
			};

			scope.selectConversation = function(c){
				scope.selectedConversation = c;
				ChatService.setCurrentConversationId(c.id);
			};

			var initController = function() {
				ChatService.setConversationsReceivedCallback(callbackConversations);
			};
			initController();			
		}
	};


}]);