'use strict';
/**
* Directive which unifies the chat components.
**/
angular.module('chatApp').directive('chatComponent', ['ChatService', function(ChatService) {

	return {
		restrict: 'E',
		templateUrl: 'views/chat/chat-component.html',
		link: function(scope, element, attrs){
			var mock = function(){
				var obj = {};
				obj['parameters'] = {'directive_type':'cotation',
                 'date_received': new Date(),
                 'proposal': {
	                 'currency': 'R$',
	                 'number_of_beneficiaries': 13,
	                 'per_day_beneficiary_value': 5,
	                 'per_month_beneficiary_value': 40,
	                 'base_value': 15 ,
	                 'total_value': 200,
	                 'expires_at': new Date(),
	                 'description': 'A refeição saborosa dos funcionários ainda traz benefícios para a sua empresa!'
                 },
                 'company': {
		              'name':"VR",
		              'picture':"http://1.bp.blogspot.com/-6Cb94AKstTI/UwOa8gJZifI/AAAAAAAABwM/JUxLJT1TlEg/s1600/VR+Refeicao.jpg"
                  },
                  'evaluations' : {
	                  'dollar_signs':4,
	                  'time':2,
	                  'hearts':4,
	                  'stars':5
                 }
                };
                console.log(obj);
				return obj.parameters;
			};

			scope.parameters = mock();			
		},
		controller: ['$scope', 'ChatService', function($scope, ChatService){
			$scope.$on('$destroy', function(){
				ChatService.destroy();
			});
		}]
	};


}]);