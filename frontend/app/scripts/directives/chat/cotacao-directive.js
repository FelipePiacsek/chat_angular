'use strict';
angular.module('chatApp').directive('cotacao', function() {

	return {
		restrict: 'EAC',
		templateUrl: 'views/chat/cotacao.html',
		scope : {
			parameters : '='
		},
		link: function(scope, element, attrs){
			var initDirective = function(){
				scope.detalhes = false;
			};
			initDirective();


		}
	};


});