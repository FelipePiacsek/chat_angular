var conversationsHost = "ws://localhost:5000/chat/";
app.factory('ConversationsSocket', function($websocket, UserData) {

      var dataStream = null;

      var _callback;

      var connectionSuccessfull = function(){
            registerCallback(_callback);
            console.log(UserData.getId() + " has connected and registered to " + conversationsHost);
      }

      this.connect = function(callback){
            var id = UserData.getId();
            if(id){
                  _callback = callback;
                  console.log("User " + id + " is connecting to " + conversationsHost + ".");
            	dataStream = $websocket(conversationsHost + id);
                  dataStream.onOpen(connectionSuccessfull);
            }
      };

      this.disconnect = function(){
            if(dataStream){
      	     dataStream.close(true);
            }
            dataStream = null;
      };

      var registerCallback = function(pointer){
            console.log("Registering callback for user " + UserData.getId());
            dataStream.onMessage(pointer);
      };

      this.send = function(object){
      	dataStream.send(object);
      };

      return this;
});