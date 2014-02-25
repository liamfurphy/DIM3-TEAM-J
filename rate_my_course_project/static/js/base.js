$(document).ready(function () {

    $('#searchform').submit(function validateSearch() {

        if ($('#searchBox').val() === "") {
            alert("Please enter a value into the search field");
            return false;
        }
        return true;
    });
});