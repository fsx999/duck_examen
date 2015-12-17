
myApp.controller('RecruitmentCtrl',
    ['$scope', '$modal', '$http', '$log', 'Etape', 'Ec', 'PersonneDsi', 'EtatHeure', 'Invitation', '$filter',
    function ($scope, $modal, $http, $log, Etape, Ec, PersonneDsi, EtatHeure, Invitation, $filter) {
    $scope.agents = [];
    $scope.monEtape = null;


    var getAgent = function(ec){

        ec.agents = ec.etat_heure;
    };
    var updateAgents = function(ec){
        EtatHeure.search(ec.code_ec).success(function(data){
            ec.agents = data;
        });
    };
    $scope.filter_invit=function(invitation){
            return invitation.date_acceptation==null;
    };
    var getInvitation = function(ec){

        ec.invitations = ec.invitation;

    };
    var updateInvitations = function(ec){
        Invitation.search(ec.code_ec).success(function(data){
            ec.invitations = data;
        });
    };
    $scope.listEc = function(etape){
        Ec.ec_by_etape(etape).success(function(data){
            $scope.ecs = data.results;

            ecs = $scope.ecs;
            for (var i = 0, length=ecs.length; i<length; i++) {
               getAgent(ecs[i]);
               getInvitation(ecs[i]);
            }
        }).error(function(data, status, headers, config) {
            $scope.ecs = 'Erreur de chargement, serveur indisponible';
        });
    };
    $scope.etapes = Etape.query(function(data) {
        $scope.etapes = $filter('filter')($scope.etapes, {cod_vrs_vet:'5'}, false);
        if($scope.etapes.length >= 1) {
            $scope.monEtape = $scope.etapes[0];
            $scope.listEc({id: $scope.etapes[0].id });
        }
    });
    $scope.$on('addPersonneDone', function(event, ec){
        updateAgents(ec);

    });
    $scope.$on('addInvitationDone', function(event, ec){
        updateAgents(ec);
        updateInvitations(ec);
    });
    $scope.$on('createInvidation', function(event, ec){

        $scope.createInvitation(ec)
    });
    $scope.searchPersonne = function(ec){
        var modalInstance = $modal.open({
            templateUrl: '/static/recruitment/app/partials/addPersonne.html',
            controller: 'SearchCtrl',
            resolve: {
                ec: function(){return ec}
            }
        });
    };
    $scope.createInvitation =  function(ec){
            var modalInstance = $modal.open({
            templateUrl: '/static/recruitment/app/partials/createInvitation.html',
                controller: 'InvitationCtrl',
                resolve: {
                     ec: function(){return ec}
                }
            });
        };
    $scope.valider_agent = function(agent){
        agent.valider = true;
        i = EtatHeure.resource().save(agent, function(){agent=i});
    };
    $scope.valider_invitation = function(invitation){
        invitation.valider = true;
        i = Invitation.resource().save(invitation, function(){invitation=i});
    };

    $scope.delete_invitation = function(invitation, ec){
        if (!invitation.valider || $scope.user.is_superuser) {
            var idx = ec.invitations.indexOf(invitation);
            i = Invitation.resource().get({InvitationEcId: invitation.id}, function () {
                i.$delete(function () {
                    ec.invitations.splice(idx, 1);
                });});}};


    $scope.delete_agent = function(agent, ec){
        if (!agent.valider || $scope.user.is_superuser) {
            var idx = ec.agents.indexOf(agent);
            i = EtatHeure.resource().get({EtatHeureId: agent.id}, function () {
                i.$delete(function () {
                    ec.agents.splice(idx, 1);
                });
            });
        }
    };

    $scope.modify_agent = function(etat_heure){

        var modalInstance = $modal.open({
            templateUrl: '/static/recruitment/app/partials/modifyPersonne.html',
            controller: 'ModifyCtrl',
            resolve: {
                etat_heure: function() { return etat_heure }
            }
        });
    };
    $scope.open_summary_download = function() {
        var modalInstance = $modal.open({
            templateUrl: '/static/recruitment/app/partials/downloadFile.html',
            controller: 'DownloadCtrl',
            resolve: {
            }
        });
    };
}]);

myApp.controller('ModifyCtrl',
    ['$scope', '$log', 'etat_heure', 'EtatHeure',
    function ($scope, $log, etat_heure, EtatHeure) {
            // $log.log(etat_heure);
            $scope.etat_heure = etat_heure;
            $scope.save = function (etat_heure) {
                EtatHeure.resource().save(etat_heure);
            }
    }]);

myApp.controller('DownloadCtrl',
    ['$scope', '$log', 'Etape', '$filter', 'Ec',
    function ($scope, $log, Etape, $filter, Ec) {
        $scope.download = function() {

        };
        $scope.data = {
            cb_ec: false,
            cb_etape: false,
            monEtape: null,
            monEc:  null,
            myUrl: '/recruitment/v1/summary',
            file_type: 'csv'
        };
        //$scope.monEtape = null;
        //$scope.monEc = null;
        $scope.etapes = Etape.query(function(data) {
            $scope.etapes = $filter('filter')($scope.etapes, {cod_vrs_vet:'5'}, false);
            if($scope.etapes.length >= 1) {
                $scope.data.monEc = null;
                $scope.data.monEtape = $scope.etapes[0];
                $scope.loadEcs({ id: $scope.etapes[0].id });
            }
        });
        $scope.ecs = {};
        $scope.loadEcs = function (etape) {
            $scope.ecs = Ec.ec_by_etape(etape).success(function(data){
                $scope.ecs = data.results;
                $scope.data.monEc = $scope.ecs[0];
            }).error(function(data, status, headers, config) {
              $scope.ecs = 'Erreur de chargement, serveur indisponible';
            });
        };
        $scope.updateUrl = function () {
            $scope.data.myUrl = '/recruitment/v1/summary';
            $scope.data.myUrl += "?type=" + $scope.data.file_type;
            if ($scope.data.cb_ec && $scope.data.cb_etape) {
                $scope.data.myUrl += '&ec=' + $scope.data.monEc
            } else if (!$scope.data.cb_ec && $scope.data.cb_etape) {
                $scope.data.myUrl += '&etape=' + $scope.data.monEtape.cod_etp;
            }
        };
        $scope.updateUrl();
    }]);

myApp.controller('SearchCtrl',
    ['$rootScope', '$scope', '$modalInstance', 'ec', '$modal', '$http', '$log', 'PersonneDsi', 'Agent', 'EtatHeure',
    function ($rootScope, $scope, $modalInstance, ec, $modal, $http, $log, PersonneDsi, Agent, EtatHeure) {

        $scope.ec = ec;
        $scope.forfaitaire = true;
        $scope.getPersonne =  function(value){
            return PersonneDsi.search(value).then(function(response){return response.data.results});
        };
        $scope.addPersonne = function(personne, ec){
            $log.log();
            a = Agent.resource().get();
            Agent
                .resource().save({
                    individu_id:personne.numero,
                    type: personne.type,
                    annee:'2015',
                    code_ec:ec.code_ec,
                    forfaitaire: $scope.forfaitaire,
                    heure: $scope.nb_heure})
                .$promise.then(function() {
                        $scope.message = {message: 'Opération réussie', type: 'success'};
                        $scope.pers = null;
                    },
                    function() {
                        $scope.message = {message: 'Il y a eu une erreur', type: 'error'};

                    }).then(function(){
                        $rootScope.$broadcast('addPersonneDone', ec);

                    });

        };
        $scope.createInvitation =  function(ec){
            $modalInstance.close();
            $rootScope.$broadcast('createInvidation', ec);
        };

}]);


myApp.controller('InvitationCtrl',
    ['$rootScope', '$scope', '$modalInstance', 'ec', 'Invitation',
    function ($rootScope, $scope, $modalInstance, ec, Invitation) {

        $scope.ec = ec;
        $scope.forfaitaire = true;
        $scope.createInvitation =  function(){
            Invitation.resource().save({ec: ec.code_ec, email: $scope.email,
                forfaitaire: $scope.forfaitaire, nombre_heure_estime: $scope.nb_heure}).$promise.then(function(){
                $rootScope.$broadcast('addInvitationDone', ec);
                $scope.errors = null;
                $scope.message = "L'invitation a bien été envoyée à l'adresse : " + $scope.email

            }, function(request){
                $scope.errors = request.data;
                    $scope.message = null;
                $rootScope.$broadcast('addInvitationDone', ec);
            });
        };

}]);