var muzik = angular.module('muzikApp', []);

muzik.controller('SelectSource', function($scope) {
    $scope.items = [
        { id: 1, name: 'soundcloud' },
        { id: 2, name: 'youtube' }
    ];

    $scope.selectedItem = null;
});

muzik.controller("FormController",function($scope, $http) {

			// create a blank object to hold our form information
			// $scope will allow this to pass between controller and view
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

angular
    .module('resultApp', [])
    .config(['$routeProvider', function($routeProvider) {
        $routeProvider
            .when('/', {
                templateUrl: 'static/result.html',
                controller: 'ResultController'
            })
            .otherwise({ redirectTo: '/' });
    }])
    .factory('windowAlert', [
        '$window',
        function($window) {
            return $window.alert;
        }
    ])
    .controller('ResultController', [
        '$scope',
        '$http',
        'windowAlert',
        function($scope, $http, windowAlert) {
               $scope.muziks = [{"name":"hello"},{"name":"world"}]



//            $scope.retrieveLastNItems = function(n) {
//                $http
//                    .get('/todoRetrieve/' + n)
//                    .success(function(data, status, headers, config) {
//                        if (data.success) {
//                            $scope.state.todoList = data.todoList;
//                        } else {
//                            windowAlert('Retrieval failed');
//                        }
//                    })
//                    .error(function(data, status, headers, config) {
//                        windowAlert("Retrieval failed");
//                    });
//            };

//            $scope.setAndRetrieveLastNItems = function(n) {
//                $scope.state.retrieveNr = n;
//                $scope.retrieveLastNItems($scope.state.retrieveNr);
//            };
        }
    ]);
//    .directive('navtabs', function() {
//        return {
//            restrict: 'E',
//            replace: true,
//            templateUrl: '../static/navtabs.html',
//            scope: {
//                pageName: '='
//            },
//            controller: [
//                '$scope',
//                function($scope) {
//                    this.selectTabIfOnPage = function(tab) {
//                        if (tab.name === $scope.pageName) {
//                            tab.selected = true;
//                        }
//                    };
//                }
//            ]
//        };
//    })
//    .directive('tab', function() {
//        return {
//            require: '^navtabs',
//            restrict: 'E',
//            replace: true,
//            transclude: true,
//            scope: {},
//            template: '<li ng-class="{ active: selected }"><a href="{{ href }}" ng-transclude></a></li>',
//            link: function(scope, element, attr, navtabsCtrl) {
//                scope.name = attr.name;
//                scope.href = attr.href;
//                scope.selected = false;
//                navtabsCtrl.selectTabIfOnPage(scope);
//            }
//        };
//    })
//    .controller('SecondController', [
//        '$scope',
//        function($scope) {
//            $scope.state = {};
//            $scope.state.pageName = 'secondPage';
//        }
//    ])
//    ;
