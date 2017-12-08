function validateAdminAdd() {
	var name = $("#name").val().trim();
	var versions = $("#versions").val().trim();
	var numversions = $("#numversions").val().trim();
	var initialrelease = $("#initialrelease").val().trim();
	var similarsoftwares = $('#similar-softwares').val().trim();

	$(".error").hide();

	if (name === "" || name === null) {
		$(".error").show();
		$(".error").html("Please enter a name");
		return false;
	}

	if (versions === "" || versions === null) {
		$(".error").show();
		$(".error").html("Versions cannot be blank");
		return false;
	}

	if (numversions === "" || numversions === null) {
		$(".error").show();
		$(".error").html("Please enter the number of versions you have entered");
		return false;
	}

	if (initialrelease === "" || initialrelease === null) {
		$(".error").show();
		$(".error").html("Please enter initial release date of the software");
		return false;
	}

	if (similarsoftwares === "" || similarsoftwares === null) {
		$(".error").show();
		$(".error").html("Please enter similar softwares");
		return false;
	}

	return true;
}
