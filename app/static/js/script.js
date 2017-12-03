var app = angular.module('vtApp', []);
app.controller('vtCtrl', function($scope, $http) {
	var status = "";
    $(".modal").modal();

    $scope.openModal = function() {
        $("#version-info").modal('open');
        console.log("hahaaaaaaaaaaaaaaaaaaaaaaa");
    }

    $scope.searchSoft = function() {
    	var software = $scope.software;
    	var version = $scope.version;

    	if (software == null || software == "" || version == "" || version == null) {
    		return;
    	}

        $(".waiting").show();

    	$http.get('/version_track/api?name=' + software + '&version=' + version).then(function(response) {
    		console.log(response.data);
            var softwareFound = response.data.software_found;
            var versionFound = response.data.version_found;
            if (softwareFound === "NOT_FOUND") {
                return;
            }

            $(".card-title").html(software + ' : ' + version);
    		$scope.latestVersion = response.data.latest_version;
    		$scope.initialVersion = response.data.initial_release;
            $scope.versions = response.data.versions;
            console.log($scope.versions);
    		
            if (versionFound === "NOT_FOUND") {
                status = "The desired version of the software is not found. Unable to provide any information. \
                          This version might not be maintained any more by the vendor or the version might be invalid."
            } else {
                if (response.data.is_obsolete === 'OBSOLETE') {
                    status = "The version you are using is " + version + ". There have been " + response.data.num_of_new_versions + " \
                              new releases. It seems that the version you are using has become obsolete. Please consider using\
                              an updated version."
                } else {
                    status = "The version you are using is " + version +".";
                    if (response.data.num_of_new_versions > 0) {
                        status += "There have been " + response.data.num_of_new_versions + "new versions released.\
                                   You may consider using an updated version of this software.";
                    } else {
                        status += "The version you are using is latest!"
                    }
                }
            }

            $scope.status = status;
            $(".waiting").hide();
            $(".intro").hide();
            $(".soft-content").show();
    	});
    }
});