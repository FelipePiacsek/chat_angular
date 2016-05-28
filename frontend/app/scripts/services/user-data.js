'use strict';
angular.module('chatApp').service('UserData',  function($localStorage){

	this.setId = function(ID){
		$localStorage.id = ID;
	};

	this.getId = function(){
		return $localStorage.id;
	};

	this.setToken = function(t){
		$localStorage.token = t;
	};
	
	this.getToken = function(){
		return $localStorage.token;
	};

	this.clearData = function(){
		$localStorage.id = null;
	};

});