'use strict';
angular.module('chatApp').directive('messagesTab', ['ChatService', function(ChatService) {

	return {
		restrict: 'E',
		templateUrl: 'views/chat/messages-tab.html',
		link: function(scope, element, attrs){
			var mock = function(){
				var messages = [];
				for(var i = 1; i <= 10; i++){
					var message = {};	
					message.id = i;
					message.sender = {};
					if (i % 3 === 0){
						message.sender.name = "Felipe Piacsek";
						message.sender.picture = "http://ytimg.googleusercontent.com/vi/jHK_387hVdQ/sddefault.jpg";
					}else{
						message.sender.name = "Pessoa " + i;
						message.sender.picture = "https://i.ytimg.com/vi/BrHAZMyN6Ok/maxresdefault.jpg";
					}
					message.ts = new Date();
					message.content = "AQUI É BODY BUILDER, PORRA.";
					message.type = 'common_text';
					message.number_of_conversationees = 7;
					messages.push(message);
				}
				return messages;
			};

			var callbackMessages = function(messages) {
				scope.messages = messages.messages;
			};
			
			var initController = function() {
				ChatService.addMessagesReceivedCallback(callbackMessages);
				//scope.messages = mock();
			};
			initController();	

			scope.isMine = function(message){
				return message.id % 3 === 0;
			};
		}
	};


}]);