'use strict';
angular.module('chatApp').directive('messagesTab', ['ChatService', 'UserData', '$timeout', function(ChatService, UserData, $timeout) {

	return {
		restrict: 'E',
		templateUrl: 'views/chat/messages-tab.html',
		link: function(scope, element, attrs){

			var time = 40;
			var scroll = function(){
				if(scope.messages && scope.messages.length > 0){
					$(".mar-btm:last-child")[0].scrollIntoView();
				}
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
				scope.messages = [];
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