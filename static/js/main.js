var muzik = angular.module('muzikApp', []);
var aaa;
muzik.config(['$routeProvider', function($routeProvider) {
        $routeProvider
            .when('/', {
                templateUrl: '../static/result.html',
                controller: 'ResultController'
            })
            .otherwise({ redirectTo: '/' });
    }])
    .controller('ResultController', function($scope,$http) {
               $scope.muziks= [];
//               $scope.muziks = [{"name":"hello","url":"http://soundcloud.com"},{"name":"world"}]
               $scope.getresult = function(){
                   $http
                    .post("/result")
                    .success(
                        function(data,status,headers,config){

                            $scope.muziks = data

                        })
                    .error(function(data, status, headers, config) {
                        });
            };
    })
    .controller("FormController",function($scope, $http) {



            $scope.selectedItem = null;
			$scope.formData = {};

            $scope.processForm = function() {
				$http({
			        method  : 'POST',
			        url     : 'submit',
			        data    : $.param($scope.formData),  // pass in data as strings
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



