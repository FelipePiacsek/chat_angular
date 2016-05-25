'use strict';
angular.module('chatApp').directive('conversationsTab', function(ChatService, ArrayUtils) {

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

			var callbackNotification = function(notification){
				c = ArrayUtils.findById(conversations, notification.data.conversation_id);
				if (scope.selectConversation.id !== notification.data.conversation_id){
					if(!c.number_of_unread_messages){
						c.number_of_unread_messages = 0;
					}
					c.number_of_unread_messages = c.number_of_unread_messages + 1;
				}
				c.last_message = notification.data.message;
			};

			scope.selectConversation = function(c){
				scope.selectedConversation = c;
				c.number_of_unread_messages = 0;
				ChatService.setCurrentConversationId(c);
			};

			var initController = function() {
				ChatService.addConversationsReceivedCallback(callbackConversations);
				ChatService.addNewMessageCallback(callbackConversations);
			};
			initController();			
		}
	};


});