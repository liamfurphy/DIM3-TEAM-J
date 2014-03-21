$(document).ready(function () {
    $("#submitbtn").click(function () {
        var username;
        var comment = $('#id_comment').val();
        $.post('/api/rating/' + $('#submitbtn').attr("val") + "/", $('#ratingform').serialize(), function (d) {

            /* Ideally we should have error checking, in case we get an error trying to add the rating */
            $("#rating_panel").html("<span id=\"submitted\">You have already submitted rating for this course</span>");
            alert("Rating added!");
            var data = d[0].data;

            /* Update the averages with new values that result from adding the rating */
            $("#number_of_ratings").html(data.ratings);
            $("#average_overall").html((data.overall).toFixed(1));
            $("#average_satisfaction").html((data.satisfaction).toFixed(1));
            $("#average_difficulty").html((data.difficulty).toFixed(1));
            $("#average_materials").html((data.materials).toFixed(1));
            $("#average_teaching").html((data.teaching).toFixed(1));

            username = data.username;
            $("#norating").remove(); /* if we were saying no rating existed before, this is no longer true now */

            $("#ratings").append("<li class=\"list-group-item clearfix\">" +
                "<div class=\"details col-xs-12 col-md-6\">" + username + "</div>" +
                "<div class=\"col-xs-12 col-md-6 ratingbreakdown\">" +
                "Overall:" + $('#id_overall_rating').find(":selected").text() +
                " Difficulty: " + $('#id_difficulty_rating').find(":selected").text() +
                " Teaching: " + $('#id_teaching_rating').find(":selected").text() +
                " Materials: " + $('#id_materials_rating').find(":selected").text() +
                " Satisfaction: " + $('#id_satisfaction_rating').find(":selected").text() +
                "</div>" +
                "<div class=\"col-xs-12 ratingcomment\">\"" + comment + "\"</div>" +
                "</li>");


        });
    });

});