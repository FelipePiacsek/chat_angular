'use strict';
angular.module('chatApp').directive('detalhesCotacao', function() {

	return {
		restrict: 'EAC',
		templateUrl: 'views/chat/detalhes-cotacao.html',
		scope : {
			parameters : '='
		},
		link: function(scope, element, attrs){

		}
	};


});