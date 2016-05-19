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
		var names = ["Felipe", "Eric", "Mariana", "Rafael", "Larissa", "Maria Thereza"]
		for(var i = 0; i < 6; i++){
			var conversation = {};
			conversation.id = i + 1;
			conversation.lastConversationee = {};
			conversation.lastConversationee.picture = null;
			conversation.lastConversationee.name = names[i];
			conversation.lastConversationee.date = new Date();
			conversation.lastMessage = {};
			conversation.lastMessage.date = new Date();
			conversation.lastMessage.text = "Texto " + i + ".";
			conversations.push(conversation);
		}
		console.log(conversations);
		return conversations;
	};

	$scope.selectConversation = function(c){
		$scope.selectedConversation = c;
	};

	var initController = function() {
		ChatService.setConversationsReceivedCallback(callbackConversations);
		//$scope.selectConversation($scope.conversations[0]);
	};
	initController();




});