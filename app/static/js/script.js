var app = angular.module('vtApp', []);
app.controller('vtCtrl', function($scope, $http) {
	var status = "";

    $scope.searchSoft = function() {
    	var software = $scope.software;
    	var version = $scope.version;

    	if (software == null || software == "" || version == "" || version == null) {
    		return;
    	}

    	$http.get('/version_track/api?name=' + software + '&version=' + version).then(function(response) {
    		console.log(response.data);
    		$scope.latestVersion = response.data.latest_version;
    		$scope.initialVersion = response.data.initial_release;
    		$scope.status = response.data.is_obsolete;
    	});
    }
});