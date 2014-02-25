$(document).ready(function () {

    $('#searchform').submit(function validateSearch() {
        var courseCode = $("#courseCode").val();
        var courseName = $("#courseName").val();
        var lecturer = $("#lecturer").val();
        var university = $("#university").val();

        if (courseCode === "" && courseName === "" && lecturer === "" && university === "") {
            alert("Please enter a value into at least one search field");
            return false;
        }

        if (courseCode === "") courseCode = "any";
        if (courseName === "") courseName = "any";
        if (lecturer === "") lecturer = "any";
        if (university === "") university = "any";

        $(this).attr("action", "/results/" + courseCode + "/" + courseName + "/" + lecturer + "/" + university + "/");
        return true;
    });
});