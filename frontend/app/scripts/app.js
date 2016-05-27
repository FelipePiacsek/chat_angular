'use strict';

/**
 * @ngdoc overview
 * @name chatApp
 * @description
 * # chatApp
 *
 * Main module of the application.
 */
var conversationsHost = "ws://localhost:5000/chat";
//var notificationsHost = "ws://localhost:5000/notifications";
var app = angular.module('chatApp', [
    'ngStorage',
    'ngResource',
    'ui.router',
    'ngWebSocket',
    'ngSanitize'
]);

app.factory('ConversationsSocket', function($websocket) {
      // Open a WebSocket for the conversations.
      var dataStream = $websocket(conversationsHost);
      return dataStream;
});
app.config(['$stateProvider', '$urlRouterProvider', function($stateProvider, $urlRouterProvider) {

    // For any unmatched url, redirect to /
    $urlRouterProvider.otherwise("/login");
}]);
app.config(function($stateProvider){
    $stateProvider.state('login', {
            url: '/login',
            templateUrl: 'views/login.html'
    });
	$stateProvider.state('chat', {
            url: '/chat',
            templateUrl: 'views/chat.html'
    });
});

// app.factory('ConversationsSocket', function($websocket) {
//       // Open a WebSocket for the conversations.
//       var dataStream = $websocket(conversationsHost);
//       return dataStream;
// });
//   .factory('NotificationsSocket', function($websocket) {
//       // Open a WebSocket for the notifications.
//       var dataStream = $websocket(notificationsHost);
//       //var dataStream = true;
//       return dataStream;
// });
