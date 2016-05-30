var conversationsHost = "ws://localhost:5000/chat/";
app.factory('ConversationsSocket', function($websocket, UserData) {

      var dataStream = null; 

      this.connect = function(){
      	dataStream = $websocket(conversationsHost + UserData.getId());
      };

      this.disconnect = function(){
      	dataStream.close();
      };

      this.onMessage = function(pointer){
            if(!dataStream){
                  this.connect();
            }
            dataStream.onMessage(pointer);
      };

      this.send = function(object){
      	dataStream.send(object);
      };

      return this;
});