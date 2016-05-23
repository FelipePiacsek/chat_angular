'use strict';
angular.module('chatApp').directive('conversationsInput', ['ChatService', function(ChatService) {

	return {
		restrict: 'E',
		templateUrl: 'views/chat/conversations-input.html',
		link: function(scope, element, attrs){
			scope.sendMessage = function(){
				var message = {};
				message.message = scope.message;
				ChatService.sendMessage(message);
				scope.message = "";
			};
		}
	};


}]);