$(document).ready(function () {
    $("#reset").click(function () {
        $.get('/api/confirm/' + $("#reset").attr("val"), function () {


        });
        alert("Email Sent!");

    })
});