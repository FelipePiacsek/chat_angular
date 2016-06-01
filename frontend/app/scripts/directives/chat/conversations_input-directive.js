'use strict';
angular.module('chatApp').directive('conversationsInput', ['ChatService', function(ChatService) {

	return {
		restrict: 'E',
		templateUrl: 'views/chat/conversations-input.html',
		link: function(scope, element, attrs){
			var getMessageType = function (message) {
				if(message.startsWith("/cotacao, ")){
					return "directive_quotation_mt";
				}
				return "common_text"
			};
			scope.sendMessage = function(){	
				var type = getMessageType(scope.message);
				ChatService.sendMessage(type, scope.message);
				scope.message = "";
			};
		}
	};


}]);