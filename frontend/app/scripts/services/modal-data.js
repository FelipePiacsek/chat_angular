'use strict'
angular.module('chatApp').service("ModalData", function() {
	
	var data = {};

	this.put = function(key, value){
		data[key] = value;
	};

	this.get = function(key){
		return data[key];
	};

	this.clear = function(){
		data = {};
	};
	
});