'use strict';

/**
 * @ngdoc function
 * @name chatApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the chatApp
 */
angular.module('chatApp').controller('MainCtrl', function ($scope, $state, HTTPService, CallbackUtils, UserData, ConversationsSocket) {

    $scope.login = function(){
    	var login = {};
    	login.email = $scope.email;
    	login.password = $scope.password;
    	HTTPService.requests('/login').post(login, function (data, responseHeaders) {
    		var id = parseInt(data.response.user.id);
            UserData.setId(id);
            ConversationsSocket.connect(id);
            $state.go("chat");
        }, function (promise) {
            CallbackUtils.mostrarErros(promise);
        });
    };

   $scope.createUser = function(){
		var endpoint = "/create_user";
		var user = {};
		user.username=$scope.email;
		user.password=$scope.password;
		user.first_name=$scope.email;
		user.last_name=$scope.email;
		user.picture=null;
		user.email=$scope.email;
		console.log(user);
	    HTTPService.requests(endpoint).post(user).$promise.then(function(response) {
	    	console.log("Usuário criado.");
	    }, function(promise) {
	        CallbackUtils.mostrarErros(promise);
	    });
   }; 

	var initController = function(){
		if(UserData.getId()){
			$state.go("chat");
		}
	};
	initController();

});
