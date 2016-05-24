'use strict';

/**
 * @ngdoc overview
 * @name chatApp
 * @description
 * # chatApp
 *
 * Main module of the application.
 */
var chatHost = "ws://localhost:5000/chat";
angular
  .module('chatApp', [
    'ngResource',
    'ngWebSocket',
    'ngSanitize'
  ])
  .factory('ChatSocket', function($websocket) {
      // Open a WebSocket connection
      var dataStream = $websocket(chatHost);
      return dataStream;
});
