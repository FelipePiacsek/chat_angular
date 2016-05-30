'use strict'
angular.module('chatApp').service("ArrayUtils", function() {
	
	this.findIndex = function(array, object, comparator) {
		var i = 0;
		if(comparator){
			for(i = 0; i < array.length; i++) {
				if(comparator(array[i], object)) {
					return i;
				}
			}
		}else{
			for(i = 0; i < array.length; i++) {
				if(array[i].id === object.id) {
					return i;
				}
			}
		}
		return -1;
	};

	this.findById = function(array, object){
		var index = this.findIndex(array, object);
		if(index < 0){
			return null;
		}
		return array[index];
	};
	
	this.remove = function(array, object, comparator) {
		var index = this.findIndex(array, object, comparator);
		array.splice(index, 1);
	};
	
});