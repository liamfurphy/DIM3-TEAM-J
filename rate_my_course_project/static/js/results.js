var results;


function GetURLParameter(sParam) {
    var sPageURL = window.location.search.substring(1);
    var sURLVariables = sPageURL.split('&');
    for (var i = 0; i < sURLVariables.length; i++) {
        var sParameterName = sURLVariables[i].split('=');
        if (sParameterName[0] == sParam) {
            return sParameterName[1];
        }
    }
}


function loadResults() {
    $(".loading").addClass("hidden");
    $(".results").removeClass("hidden");
    $(".results").empty();

    if (results.length === 0) {
        $(".results").append("<li class='list-group-item noresults clearfix'>No results found.</li>")

        return;
    }

    $(".results-container").removeClass("col-md-12");
    $(".results-container").addClass("col-md-10");

    if ($("#rating-sort").attr("value") !== null) {
        results.sort(function (a, b) {
            var field = $("#rating-sort").attr("value");
            var asc = $("#asc").attr("value");
            if (field == "Overall Rating") {

                if (asc == "Ascending") return a.average_overall - b.average_overall;
                return b.average_overall - a.average_overall;
            }
            else if (field == "Satisfaction Rating") {
                if (asc == "Ascending") return a.average_satisfaction - b.average_satisfaction;
                return b.average_satisfaction - a.average_satisfaction;
            }
            else if (field == "Difficulty Rating") {
                if (asc == "Ascending") return a.average_difficulty - b.average_difficulty;
                return b.average_difficulty - a.average_difficulty;
            }
            else if (field == "Teaching Rating") {
                if (asc == "Ascending") return a.average_teaching - b.average_teaching;
                return b.average_teaching - a.average_teaching;
            }
            else if (field == "Materials Rating") {
                if (asc == "Ascending") return a.average_materials - b.average_materials;
                return b.average_materials - a.materials_rating;
            }
        });
    }

    $(".filters").removeClass("hidden");

    for (var i = 0; i < results.length; i++) {
        $(".results").append('<li class="list-group-item course clearfix">' +
            '<div class="details col-xs-12 col-lg-10">' +
            '<a href="/summary/course/' + results[i].course_id + '/" class="courselink">' + results[i].course_code + '<br/>' +
            results[i].course_name + '</a><br/>' +
            results[i].lecturer + '<br/>' +
            '<a href="/summary/uni/' + results[i].uni_id + '" class="unilink">' + results[i].uni + '</a>' +
            '</div>' +
            '<div class="rating col-lg-2 clearfix">' + ((results[i].average_overall == null) ? "None" : results[i].average_overall) + '</div>' +
            '</li>');
    }
}


$(document).ready(function () {


    $.get("/api/results/" + GetURLParameter("s").replace("+", "_"), function (data) {
        results = data;
        loadResults();
    });

    $(".dropdown-menu li a").click(function () {
        var txt = $(this).text();
        $(this).closest(".btn-group").children().first().val($(this).text());
        $(this).closest(".btn-group").children().first().text($(this).text());
        $(this).closest(".btn-group").children().first().append('<span class="caret"></span>');
        loadResults();
    });


})
;