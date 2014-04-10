var muzik = angular.module('muzikApp', []);

muzik.config(['$routeProvider', function($routeProvider) {
        $routeProvider
            .when('/', {
                templateUrl: '../static/result.html',
                controller: 'ResultController'
            })
            .otherwise({ redirectTo: '/' });
    }])
    .controller('ResultController', function($scope) {
               $scope.muziks = [{"name":"hello"},{"name":"world"}]
    })
    .controller("FormController",function($scope, $http) {

            $scope.items = [
            { id: 1, name: 'soundcloud' },
            { id: 2, name: 'youtube' }
            ];

            $scope.selectedItem = null;
			$scope.formData = {};

			// process the form
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



