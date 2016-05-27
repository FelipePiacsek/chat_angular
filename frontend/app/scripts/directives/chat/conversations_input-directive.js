'use strict';
angular.module('chatApp').directive('conversationsInput', ['ChatService', function(ChatService) {

	return {
		restrict: 'E',
		templateUrl: 'views/chat/conversations-input.html',
		link: function(scope, element, attrs){
			scope.sendMessage = function(){
				if(scope.message==="criar_usuario"){
					ChatService.createUser();
				}else{
					ChatService.sendTextMessage(scope.message);
					scope.message = "";
				}
			};
		}
	};


}]);