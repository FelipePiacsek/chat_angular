'use strict';
/**
* Directive which unifies the chat components.
**/
angular.module('chatApp').directive('chatComponent', ['ChatService', function(ChatService) {

	return {
		restrict: 'E',
		templateUrl: 'views/chat/chat-component.html',
		link: function(scope, element, attrs){
			
		}
	};


}]);