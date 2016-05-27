angular.module('chatApp').service('HTTPService', ['$resource', 'Environment',  function($resource, Environment) {

    this.requests = function(endpoint){
        return this.requests(endpoint, {});
    };
    this.requests = function(suffix, queryParameters){
        var token = "token"; //AuthData.getToken();
        var builtEndpoint = Environment.buildEndpoint(suffix);
        return $resource(builtEndpoint, queryParameters,{
            post:{
                method:"POST",
                isArray:false
                //headers:{'Content-Type' : 'application/json'}
                //,headers:{'token' : token}
            },
            get:{
                method:"GET",
                isArray:false
                //,headers:{'token' : token}
            },
            update:{
                method:"PUT",
                isArray:false
                //,headers:{'token' : token}
            },
            remove:{
                method:"DELETE",
                isArray:false
                //,headers:{'token' : token}
            },
            getAll:{
                method:"GET",
                isArray:true
                //,headers:{'token' : token}
            },
            postMultipart:{
                method:"POST",
                transformRequest: angular.identity,
                isArray:false
                //,headers:{'token' : token}
            }
        });
    };
}]);