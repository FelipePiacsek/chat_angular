'use strict';
angular.module('chatApp').directive('conversationsTab', function($rootScope, ChatService, ArrayUtils, ModalData) {

	return {
		restrict: 'E',
		templateUrl: 'views/chat/conversations-tab.html',
		link: function(scope, element, attrs){
			var callbackConversations = function(conversations) {
				if(conversations.conversations){
					scope.conversations = conversations.conversations;
					for (var i = 0; i < scope.conversations.length; i++){
						scope.conversations[i].last_message.ts = new Date(scope.conversations[i].last_message.ts);
					}
					scope.selectConversation(scope.conversations[0]);
				}
			};

			var callbackNotification = function(notification){
				var index = ArrayUtils.findIndex(scope.conversations, notification.conversation_id, function(a, b){return a.id == b});
				var c = scope.conversations[index];
				if (scope.selectedConversation.id === notification.conversation_id){
					ChatService.markAsRead(notification);
				}
				c.number_of_unread_messages = notification.number_of_unread_messages;
				c.last_message = notification;
			};

			scope.selectConversation = function(c){
				scope.selectedConversation = c;
				c.number_of_unread_messages = 0;
				ChatService.setCurrentConversationId(c);
			};

			scope.openNewConversationModal = function(type){
				$rootScope.conversationType = type;
				ModalData.put('type', type);
				$('#new-conversation-modal').modal('show');
			};

			var initController = function() {
				ChatService.addConversationsReceivedCallback(callbackConversations);
				ChatService.addNewMessageCallback(callbackNotification);
			};
			initController();			
		}
	};


});