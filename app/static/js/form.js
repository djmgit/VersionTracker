function verifyAdminAdd() {

	var name = $("#name").val();
	var verions = $("#versions").val();
	var numversions = $("#numversions").val();
	var initialrelease = $("#initialrelease").val();
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

	return true;
}