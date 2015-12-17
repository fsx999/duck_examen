/**
 * Created by paulguichon on 06/10/2015.
 */

var servicesRecrutement = angular.module('servicesRecrutement', ['ngResource']);

servicesRecrutement.factory('Etape', ['$resource',
    function($resource){
        return $resource('/recruitment/v1/etapes/:etapeId', {}, {
            query: {method: 'GET', params: {etapeId: '@etapeId'}, isArray: true}
        })
    }]);


servicesRecrutement.factory('Ec', ['$resource', '$http',
    function($resource, $http){
        var resource = function(){
            return $resource('/recruitment/v1/ecs/:ecId', {}, {
            query: {method: 'GET', params: {ecId: '@ecId'}, isArray: true}
            });
        };
        var ec_by_etape = function(etape){
            return $http.get('/recruitment/v1/ecs', {params: {etape: etape.id}, isArray: true});
        };
        return {resource: resource, ec_by_etape: ec_by_etape}
    }]);

servicesRecrutement.factory('PersonneDsi', ['$resource', '$http', function($resource, $http){
    var resource = function(){ return $resource('/recruitment/v1/dsi-individus/:individuId', {}, {
        query: {method: 'GET', params: {individuId: '@individuId'}, isArray: true}
    })};
    var search = function(val){
        return $http.get('/recruitment/v1/dsi-individus', {params: {nom_pat: val}, isArray: true});
    };
    return {resource: resource, search: search}
}]);

servicesRecrutement.factory('Agent', ['$resource', '$http', function($resource, $http){
    var resource = function(){
        return $resource('/recruitment/v1/agents/:agentId',{}, {
           query:  {method: 'GET', params: {agentId: '@agentId'}, isArray: true}
        });
    };
    return {resource: resource}
}]);

servicesRecrutement.factory('EtatHeure', ['$resource', '$http', function($resource, $http){
    var resource = function(){
        return $resource('/recruitment/v1/etat_heure/:EtatHeureId',{}, {
           query:  {method: 'GET', params: {EtatHeureId: '@EtatHeureId'}, isArray: true},
            delete: { method: 'DELETE', params: {EtatHeureId: '@id'} }
        });
    };
    var search = function(val){
        return $http.get('/recruitment/v1/etat_heure', {params: {ec: val}, isArray: true});
    };
    return {resource: resource, search: search}
}]);

servicesRecrutement.factory('Invitation', ['$resource', '$http', function($resource, $http){

    var resource = function(){
        return $resource('/recruitment/v1/invitations_ec/:InvitationEcId',{}, {
           query:  {method: 'GET', params: {InvitationEcId: '@InvitationEcId'}, isArray: true},
            delete: { method: 'DELETE', params: {InvitationEcId: '@id'} }
        });
    };
    var search = function(val){
        return $http.get('/recruitment/v1/invitations_ec', {params: {ec: val}, isArray: true});
    };
    return {resource: resource, search: search}
}]);