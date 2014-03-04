$(document).ready(function () {

    $('.ratingbreakdown').each(function () {
        var num = $(this).attr("id").slice(6);
        $("#rating" + num).click(function () {
            $("#ratingpanel" + num).slideToggle();
        });
    });
});