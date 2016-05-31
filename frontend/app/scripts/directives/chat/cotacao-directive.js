'use strict';
angular.module('chatApp').directive('cotacao', function() {

	return {
		restrict: 'E',
		templateUrl: 'views/chat/cotacao.html',
		scope : {
			parameters : '='
		},
		link: function(scope, element, attrs){
			
		}
	};


});