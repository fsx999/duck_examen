var myApp = angular.module('myApp', [
    'ngRoute',
    'servicesRecrutement',
    'ui.bootstrap'
]);

myApp.config(['$routeProvider', '$httpProvider',
    function ($routeProvider, $httpProvider) {
        $routeProvider.
            when('/', {
                templateUrl: '/static/examens/app/partials/home.html',
                controller: 'ExamenCtrl'
            }).
            when('/centre_rattachement', {
                templateUrl: '/static/examens/app/partials/rattachement.html',
                controller: 'RattachementCtrl'
            }).
            otherwise({
                redirectTo: '/'
            });
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    }]);

//myApp.run(['$rootScope', '$http', function($rootScope, $http){
//    $http.get('/recruitment/v1/users').success(function(data){
//       if(data.length == 1){
//           $rootScope.user = data[0];
//       }
//    });
//}
//
//]);
