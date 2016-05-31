var conversationsHost = "ws://localhost:5000/chat/";
app.factory('ConversationsSocket', function($websocket, UserData) {

      var dataStream = null; 

      var connectionSuccessfull = function(){
            console.log(UserData.getId() + " has connected to " + conversationsHost);
      }

      this.connect = function(){
            var id = UserData.getId();
            console.log("User " + id + " is connecting to " + conversationsHost + ".");
      	dataStream = $websocket(conversationsHost + id);
            dataStream.onOpen(connectionSuccessfull);
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