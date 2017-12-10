var app = angular.module('exApp', []);
app.controller('exCtrl', function($scope, $http) {
	$scope.initialReleas = "";
    $scope.latestRelease = "";
    console.log("jaja");

    $scope.search = function() {
        var name = $scope.name;
        var version = $scope.version;
        console.log("haha");
        alert("haha");

        if (name == '' || version == '') {
            return;
        }

        $http.jsonp('https://version-tracker.herokuapp.com/version_track/api?name=' + name + '&version=' + version).then(function(response) {
            console.log(response.data);
        });
    }
});