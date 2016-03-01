
myApp.controller('ExamenCtrl',
    ['$scope', '$http', 'DuckExamen',
        function ($scope, $http, DuckExamen) {
            $scope.env = {};
            $scope.env.isLoaded = false;
            $scope.env.currentPage = 1;
            $scope.env.data = {count: 0, results: [], dirty: true};
            $scope.env.searchPattern = "";
            $scope.env.currentView = "home";
            //$scope.v.currentView = "home";
            $scope.env.currentRecord = null;
            $scope.changePage = function () {
                $scope.env.isLoaded = false;
                DuckExamen.loadData($scope.env.currentPage, $scope, $scope.env.searchPattern);
            };

            $scope.formatRattachements = function(rattachements) {
                var result = "";
                for (var i = 0, l = rattachements.length; i < l; ++i) {
                    result += "Session " + rattachements[i].session + ": ";
                    result += rattachements[i].centre_label;
                    result += ". Ec manquant: " + (rattachements[i].ec_manquant === true ? "Oui" : "Non")  + "\n";
                }
                return result;
            };
            init = function () {
                $scope.env.isLoaded = false;
                DuckExamen.loadData($scope.env.currentPage, $scope, $scope.env.searchPattern);
            };
            init();

            $scope.onSearchPatternChange = function () {
                $scope.env.isLoaded = false;
                $scope.env.currentPage = 1;
                DuckExamen.loadData($scope.env.currentPage, $scope, $scope.env.searchPattern);
                $scope.env.currentSearchPattern = $scope.env.searchPattern;
            };

            $scope.mouseover = function (blop) {
                console.log(blop);
            };
            $scope.changeView = function (viewName, data) {
                $scope.env.currentView = viewName;
                if (typeof(data) != 'undefined') {
                    $scope.env.currentRecord = data;
                }

            };

            $scope.formatPrenoms = function(individu) {
                return (individu.lib_pr1_ind +
                        (individu.lib_pr2_ind != "" ? (" " + individu.lib_pr2_ind ) : "") +
                        (individu.lib_pr3_ind != "" ? (" " + individu.lib_pr3_ind): ""));
            };

            $scope.formatNoms = function(individu) {
                return (individu.lib_nom_pat_ind +
                        (individu.lib_nom_usu_ind != "" ? (" (" + individu.lib_nom_usu_ind + ")") : "" ));
            };


        }

    ]);

myApp.factory('DuckExamen', ['$http', '$resource', function ($http, $resource) {
    var obj = {};
    obj.loadData = function(page, $scope, searchPattern) {
            var url = '/examen/api/v1/DuckExamen/?page='+page;
            if (searchPattern != "") {
                url += "&search=" + searchPattern
            }
            data = $resource(url, {}, {
                query: {method: 'GET', params: {}, isArray: false}
            });
            data.query(function(response) {
                $scope.env.data = response;
                $scope.env.isLoaded = true;
            });
        };
    return obj
}]);


//myApp.controller('RattachementCtrl',
//    ['$scope', '$http', 'DuckExamen',
//       function ($scope, $http, DuckExamen) {
//
//        }
//
//    ]);

myApp.directive('individuReadOnly', function() {
    return {
        templateUrl: "/static/examens/app/partials/individu_read_only.html"
    };
});

myApp.directive('rattachementsCentreExamen', function() {
    return {
        templateUrl: "/static/examens/app/partials/rattachements_centre_examen.html"
    };
});


//myApp.controller('BlogCtrl', ['$scope', 'Blog', function($scope, Blog) {
//    Blog.Posts.query(function(response) { $scope.posts = response });
//}]);

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