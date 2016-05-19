'use strict';
angular.module('chatApp').controller('ConversationsListController', function(ChatService, $scope) {
	
	var callbackConversations = function(conversations) {
		$scope.conversations = conversations.conversations;
		for (var i = 0; i < $scope.conversations.length; i++){
			$scope.conversations[i].last_message.date = new Date($scope.conversations[i].last_message.date);
		}
		console.log($scope.conversations);
	};

	var mock = function(){
		var conversations = [];
		var names = ["Felipe Macedo Piacsek", "Eric Ijiri Santiago", "Mariana Lopes Melo Franco", "Rafael Vaini de Souza", "Larissa Montezano", "Maria Thereza Sichi Machado"]
		for(var i = 0; i < 6; i++){
			var conversation = {};
			conversation.conversation_id = i + 1;
			conversation.last_conversationee = {};
			conversation.last_conversationee.picture = null;
			conversation.last_conversationee.name = names[i];
			conversation.last_conversationee.date = new Date();
			conversation.last_message = {};
			conversation.last_message.date = new Date();
			conversation.last_message.text = "Texto " + i + ".";
			conversations.push(conversation);
		}
		console.log(conversations);
		return conversations;
	};

	$scope.selectConversation = function(c){
		$scope.selectedConversation = c;
	};

	var initController = function() {
		//ChatService.setConversationsReceivedCallback(callbackConversations);
		$scope.conversations = mock();
		$scope.selectConversation($scope.conversations[0]);
	};
	initController();




});