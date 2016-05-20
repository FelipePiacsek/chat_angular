'use strict';
angular.module('chatApp').directive('conversationsTab', ['ChatService', function(ChatService) {

	return {
		restrict: 'E',
		templateUrl: 'views/chat/conversations-tab.html',
		link: function(scope, element, attrs){
			
		}
	};


}]);