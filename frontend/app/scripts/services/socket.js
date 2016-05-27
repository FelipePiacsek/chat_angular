var conversationsHost = "ws://localhost:5000/chat/";
app.factory('ConversationsSocket', function($websocket) {

      var dataStream = null; 

      this.connect = function(id){
      	dataStream = $websocket(conversationsHost + id);
      };

      this.disconnect = function(){
      	dataStream.close();
      };

      this.onMessage = function(pointer){
      	dataStream.onMessage(pointer);
      };

      this.send = function(object){
      	dataStream.send(object);
      };

      return this;
});