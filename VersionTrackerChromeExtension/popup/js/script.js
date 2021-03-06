var app = angular.module('exApp', []);
app.controller('exCtrl', function($scope, $http) {
	$scope.initialReleas = "";
    $scope.latestRelease = "";

    $(".not-found").hide();

    $scope.viewReleases = function() {
        $(".similar").hide();
        $(".versions").toggle();
    }

    $scope.viewSimilar = function() {
        $(".similar").toggle();
        $(".versions").hide();
    }

    $scope.search = function() {
        var name = $scope.name;
        var version = $scope.version;
        console.log("haha");

        if (name == '' || version == '') {
            return;
        }

        $http.get('https://version-tracker.herokuapp.com/version_track/api?name=' + name + '&version=' + version).then(function(response) {
            console.log(response.data);
            var status = "";

            var softwareFound = response.data.software_found;
            var versionFound = response.data.version_found;
            if (softwareFound === "NOT_FOUND") {
                
                $(".intro").hide();
                $(".not-found").show();
                $(".main-info").hide();
                return;
            }

            
            $scope.latestRelease = response.data.latest_version;
            $scope.initialRelease = response.data.initial_release;
            $scope.versions = response.data.versions;
            $scope.similarSoftwares = response.data.similar_softwares;
            console.log($scope.versions);
            
            if (versionFound === "NOT_FOUND") {
                status = "The desired version of the software is not found. Unable to provide any information. \
                          This version might not be maintained any more by the vendor or the version might be invalid.";

            } else {
                if (response.data.is_obsolete === 'OBSOLETE') {
                    status = "The version you are using is " + version + ". There have been " + response.data.num_of_new_versions + " \
                              new releases. It seems that the version you are using has become obsolete. Please consider using\
                              an updated version.";
                } else {
                    status = "The version you are using is " + version +".";
                    if (response.data.num_of_new_versions > 0) {
                        status += "There have been " + response.data.num_of_new_versions + "new versions released.\
                                   You may consider using an updated version of this software.";
                    } else {
                        status += "The version you are using is latest!";
                    }
                }
            }

            $scope.status = status;
            $(".intro").hide();
            $(".not-found").hide();
            $(".main-info").show();
        });
    }
});