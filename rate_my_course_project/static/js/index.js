$(document).ready(function () {

    $('.ratingbreakdown').each(function () {
        var num = $(this).attr("id").slice(6);
        console.log(num);
        $("#rating" + num).click(function () {
            console.log("HELLO!");
            $("#ratingpanel" + num).slideToggle();
        });
    });
});