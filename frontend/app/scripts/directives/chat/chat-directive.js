'use strict';
/**
* Directive which unifies the chat components.
**/
angular.module('chatApp').directive('chatComponent', ['ChatService', function(ChatService) {

	return {
		restrict: 'E',
		templateUrl: 'views/chat/chat-component.html',
		link: function(scope, element, attrs){
			
		},
		controller: ['$scope', 'ChatService', function($scope, ChatService){
			$scope.$on('$destroy', function(){
				ChatService.destroy();
			});
		}]
	};


}]);