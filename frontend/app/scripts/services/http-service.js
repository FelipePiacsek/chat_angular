angular.module('chatApp')
    .service('HTTPService', ['$resource',  function($resource) {

    this.requests = function(endpoint){
        return this.requests(endpoint, {});
    };
    this.requests = function(endpoint, queryParameters){
        var token = "token"; //AuthData.getToken();
        return $resource('http://localhost:5000' + endpoint, queryParameters,{
            post:{
                method:"POST",
                isArray:false,
                headers:{'token' : token}
            },
            get:{
                method:"GET",
                isArray:false,
                headers:{'token' : token}
            },
            update:{
                method:"PUT",
                isArray:false,
                headers:{'token' : token}
            },
            remove:{
                method:"DELETE",
                isArray:false,
                headers:{'token' : token}
            },
            getAll:{
                method:"GET",
                isArray:true,
                headers:{'token' : token}
            },
            postMultipart:{
                method:"POST",
                transformRequest: angular.identity,
                isArray:false,
                headers:{'token' : token}
            }
        });
    };
}]);