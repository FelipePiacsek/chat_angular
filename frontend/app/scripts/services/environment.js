'use strict';
angular.module('chatApp').service('Environment',  function(){

	var currentMode = "development"
	
	this.setProductionMode = function(){
		currentMode = "production";
	};

	this.setDevelopmentMode = function(){
		currentMode = "development";
	};

	this.buildEndpoint = function(suffix){
		if(!suffix){
			throw "You must inform a valid endpoint suffix."
		}
		var prefix = 'undefined';
		var endpoint = null;
		if (currentMode === "development"){
			prefix = "http://localhost:5000/"
		}
		if (suffix.startsWith('/')){
			endpoint = prefix + suffix.substring(1);
		}else{
			endpoint = prefix + suffix;
		}
		return endpoint;
	};

});