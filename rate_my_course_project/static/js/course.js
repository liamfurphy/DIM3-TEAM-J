$(document).ready(function () {
    $("#submitbtn").click(function () {
        var username;
        $.post('/api/rating/' + $('#submitbtn').attr("val") + "/", $('#ratingform').serialize(), function (d) {
            var data = d[0].data;
            //[{"data": {"ratings": 9, "overall": 1, "satisfaction": 1, "difficulty": 1, "materials": 1, "teaching": 1}}]
            $("#number_of_ratings").html(data.ratings);
            $("#average_overall").html((data.overall).toFixed(1));
            $("#average_satisfaction").html((data.satisfaction).toFixed(1));
            $("#average_difficulty").html((data.difficulty).toFixed(1));
            $("#average_materials").html((data.materials).toFixed(1));
            $("#average_teaching").html((data.teaching).toFixed(1));
            console.log(data);
            username = data.username;

            $("#ratings").append("<li class=\"list-group-item clearfix\">" +
                "<div class=\"details col-xs-12 col-md-6\">" + username + "</div>" +
                "<div class=\"col-xs-12 col-md-6 ratingbreakdown\">" +
                "Overall:" + $('#id_overall_rating').find(":selected").text() +
                " Difficulty: " + $('#id_difficulty_rating').find(":selected").text() +
                " Teaching: " + $('#id_teaching_rating').find(":selected").text() +
                " Materials: " + $('#id_materials_rating').find(":selected").text() +
                " Satisfaction: " + $('#id_satisfaction_rating').find(":selected").text() +
                "</div>" +
                "<div class=\"col-xs-12 ratingcomment\">\"" + $('#id_comment').text() + "\"</div>" +
                "</li>");
            $("#rating_panel").html("<span id=\"submitted\">You have already submitted rating for this course</span>");
            alert("Rating added!");

        });
    });

});