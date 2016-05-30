'use strict';
angular.module('chatApp').directive('messagesTab', ['ChatService', 'UserData', '$timeout', function(ChatService, UserData, $timeout) {

	return {
		restrict: 'E',
		templateUrl: 'views/chat/messages-tab.html',
		link: function(scope, element, attrs){

			var time = 40;
			var scroll = function(){
				$(".mar-btm:last-child")[0].scrollIntoView()
			};
			var callbackMessages = function(messages) {
				scope.messages = messages.messages;
				$timeout(scroll, time);
			};

			var newSingleMessageCallback = function(message){
				scope.messages.push(message);
				$timeout(scroll, time);
			};
			
			var initController = function() {
				ChatService.addMessagesReceivedCallback(callbackMessages);
				ChatService.addNewMessageCallback(newSingleMessageCallback);
			};
			initController();	

			scope.isMine = function(message){
				return message.sender.id === UserData.getId();
			};
		}
	};


}]);