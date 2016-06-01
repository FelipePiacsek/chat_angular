'use strict';
angular.module('chatApp').service('ChatMessageFactory',  function(){



	var buildCotacaoDirective = function(parameters, currentConversationId){
		parameters = parameters.replace("/cotacao, ", "");
		var arrayParameters = parameters.split(", ");

		var message = {};
		message.type_name = "directive_quotation_mt";
		message.conversation_id = currentConversationId;
		message.args  = {};
		message.args.currency = arrayParameters[0];
		message.args.per_day_beneficiary_value = arrayParameters[1];
		message.args.number_of_beneficiaries = arrayParameters[2];
		message.args.company_name = arrayParameters[3];
		message.args.company_picture = "";

		return message;
	};

	var buildTextMessage = function(text, currentConversationId){
		var message = {};
		message.args = {};
		message.args.text = text;
		message.type_name = "common_text";
		message.file = null;
		message.conversation_id = currentConversationId;
		return message;
	};

	this.buildMessage = function(type, parameters, currentConversationId){
		return builders[type](parameters, currentConversationId);
	};

	var builders = {};
	var initService = function(){
		builders['directive_quotation_mt'] = buildCotacaoDirective;
		builders['common_text'] = buildTextMessage;
	};
	initService();

});