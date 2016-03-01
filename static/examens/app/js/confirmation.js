/**
 * Created by paulguichon on 10/10/2015.
 */
var myApp = angular.module('confirmationApp', [
    'ngRoute',
    'ui.bootstrap'
]).
    constant('SERVEUR', {
        base_url: '/recruitement/v1/',
        base_template: '/static/recruitment/app/partials/'
    });

myApp.config(['$routeProvider', '$httpProvider',
    function ($routeProvider, $httpProvider) {
        $routeProvider.
            when('/', {
                templateUrl: '/static/recruitment/app/partials/formulaire_confirmation.html',
                controller: 'ConfirmationCtrl'
            }).
            otherwise({
                redirectTo: '/'
            });
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    }]);

myApp.controller('ConfirmationCtrl',
    ['$scope', '$http', '$log', '$location',
    function ($scope, $http, $log, $location) {
        var invitation;

        searchEc = function(){
            invitation = $location.absUrl().split('/').slice(-3, -2)[0];
            return $http.get('/recruitment/v1/invitations_ec/'+invitation);
        };
        searchEc().then(function(request){
            $scope.invitation = request.data;
            $http.get('/recruitment/v1/ecs/'+request.data.ec).then(function(request){
                $scope.ec =request.data;
            });});
        $scope.personne=null;
        $scope.searchPersonne = function(numero){
             $http.get('/recruitment/v1/dsi-individus', {params: {numero: numero}, isArray: true}).success(function(data){

                 if (data.results.length == 1){
                     $scope.numero = numero;
                     $scope.personne = data.results[0];
                 }
             });
        };
        $scope.reset = function(){
              $scope.personne=null;
        };
        $scope.confirme_personne = function(numero){
            $http.post('/recruitment/v1/confirme_invitation', {numero: $scope.numero, id: invitation }).then(function(request){
               $scope.invitation = request.data;

            }, function(request){
                $scope.errors = "Il y a eu une erreur sur le serveur, le service informatique intervient au plus vite pour la résoudre";
            });
        }


}]);


