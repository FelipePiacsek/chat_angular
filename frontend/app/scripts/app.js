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
angular
  .module('chatApp', [
    'ngResource',
    'ngWebSocket',
    'ngSanitize'
  ])
  .factory('ConversationsSocket', function($websocket) {
      // Open a WebSocket for the conversations.
      var dataStream = $websocket(conversationsHost);
      return dataStream;
});
//   .factory('NotificationsSocket', function($websocket) {
//       // Open a WebSocket for the notifications.
//       var dataStream = $websocket(notificationsHost);
//       //var dataStream = true;
//       return dataStream;
// });
