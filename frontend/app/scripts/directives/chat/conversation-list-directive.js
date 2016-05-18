'use strict';
angular.module('chatApp').directive('conversationList', ['ChatService', function(ChatService) {

	return {
		restrict: 'E',
		templateUrl: 'views/chat/conversation-list.html',
		link: function(scope, element, attrs){
			
		}
	};


}]);