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
    'ngRoute',
    'ngWebSocket',
    'ngSanitize'
  ])
  .config(function ($routeProvider) {
    $routeProvider
      .when('/', {
        templateUrl: 'views/main.html',
        controller: 'MainCtrl',
        controllerAs: 'main'
      })
      .otherwise({
        redirectTo: '/'
      });
  })
  .factory('ChatSocket', function($websocket) {
      // Open a WebSocket connection
      var dataStream = $websocket(chatHost);

      var collection = [];

      dataStream.onMessage(function(message) {
        collection.push(JSON.parse(message.data));
      });

      var methods = {
        collection: collection,
        get: function() {
          dataStream.send(JSON.stringify({ action: 'get' }));
        },
        sendMessage: function(message){
          dataStream.send(message);
        }
      };

      return methods;
  })
