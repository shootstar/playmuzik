var muzik = angular.module('muzikApp', []);
muzik
    .config(['$routeProvider', function($routeProvider) {
        $routeProvider
            .when('/', {
                templateUrl: '../static/result.html',
                controller: 'ResultController'
            })
    }])
    .factory('UserService', function() {
        return {
            items :  [
                                { id: 1, name: 'soundcloud',url:"http://soundcloud.com" },
                                { id: 2, name: 'youtube' ,url:"http://youtube.com"}
                            ]
        };
    })
    .controller('ResultController', [
        '$scope',
        '$http',
        function($scope, $http) {
               $scope.muziks = [{"name":"hello"},{"name":"world"}]
        }
    ])
    .controller("FormController",function($scope, $http) {
            console.log("aaaaaaaaa")
			// create a blank object to hold our form information
			// $scope will allow this to pass between controller and view
			$scope.items = [
                                                           { id: 1, name: 'soundcloud',url:"http://soundcloud.com" },
                                                           { id: 2, name: 'youtube' ,url:"http://youtube.com"}
                                                       ];

            $scope.selectedItem = null;
			$scope.formData = {};

			// process the form
			$scope.go = function() {
			    console.log("processform");
			    console.log( $scope.formData.source);
				$http({
			        method  : 'POST',
			        url     : 'submit',
			        data    : $scope.formData,  // pass in data as strings
			        headers : { 'Content-Type': 'application/x-www-form-urlencoded' }  // set the headers so angular passing info as form data (not request payload)
			    })
			        .success(function(data) {
			            console.log(data);

			            if (!data.success) {
			            	// if not successful, bind errors to error variables
			                //$scope.errorName = data.errors.name;
			                //$scope.errorSuperhero = data.errors.superheroAlias;
                           // $scope.errorForm = data.errors;
			            } else {
			            	// if successful, bind success message to message
			                //$scope.message = data.message;
			            }
			        });

			};
});



