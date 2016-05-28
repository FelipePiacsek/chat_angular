angular.module('chatApp').service('HTTPService', ['UserData', '$resource', 'Environment',  function(UserData, $resource, Environment) {

    this.requests = function(endpoint){
        return this.requests(endpoint, {});
    };
    this.requests = function(suffix, queryParameters){
        var token = UserData.getToken();
        var builtEndpoint = Environment.buildEndpoint(suffix);
        return $resource(builtEndpoint, queryParameters,{
            post:{
                method:"POST",
                isArray:false,
                headers:{'Authentication-Token' : token}
            },
            get:{
                method:"GET",
                isArray:false,
                headers:{'Authentication-Token' : token}
            },
            update:{
                method:"PUT",
                isArray:false,
                headers:{'Authentication-Token' : token}
            },
            remove:{
                method:"DELETE",
                isArray:false,
                headers:{'Authentication-Token' : token}
            },
            getAll:{
                method:"GET",
                isArray:true,
                headers:{'Authentication-Token' : token}
            },
            postMultipart:{
                method:"POST",
                transformRequest: angular.identity,
                isArray:false,
                headers:{'Authentication-Token' : token}
            }
        });
    };
}]);