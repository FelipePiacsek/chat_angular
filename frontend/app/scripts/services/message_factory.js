'use strict';
angular.module('chatApp').service('MessageFactory',  function(UserData){

	this.buildTextMessage = function(text, currentConversationId){
		var message = {};
		message.args = {};
		message.args.text = text;
		message.type_name = "common_text";
		message.file = null;
		message.conversation_id = currentConversationId;
		message.sender_id = UserData.getId();
		return message;
	};

});