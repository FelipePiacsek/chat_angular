'use strict';

/**
 * @ngdoc function
 * @name chatApp.controller:AboutCtrl
 * @description
 * # AboutCtrl
 * Controller of the chatApp
 */
angular.module('chatApp').controller('AboutCtrl', function ($scope, $state, UserData, ChatService) {
    $scope.logout = function(){
    	ChatService.destroy();
    	UserData.clearData();
    	$state.go("login");
    };
});
