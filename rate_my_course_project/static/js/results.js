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

var asc = "Ascending";
var uni = [];
var overall=[0, 100];
var diff = [0, 100];
var sat = [0, 100];
var mat = [0, 100];
var teac = [0, 100];
var lec = [];

function loadResults() {
    $(".loading").addClass("hidden");
    $(".results").removeClass("hidden");
    $(".results").empty();
    $(".results-container").addClass("col-md-8");

    if (results.length === 0) {
        $(".results").append("<li class='list-group-item noresults clearfix'>No results found.</li>")

        return;
    }

    $(".results-container").removeClass("col-md-12");
    $(".results-container").addClass("col-md-10");

    if ($("#rating-sort").attr("value") !== null) {
        results.sort(function (a, b) {
            if (a.average_overall == null) {
                return (asc == "Ascending") ? -1 : 1;
            }
            else if (b.average_overall == null) {
                return (asc == "Ascending") ? 1 : -1;
            }
            var field = $("#rating-sort").attr("value");
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
    var match = 0;
    for (var i = 0; i < results.length; i++) {
        if ((lec.length == 0 || lec.indexOf(results[i].lecturer) != -1) && (uni.length == 0 || uni.indexOf(results[i].uni) != -1) &&
            (results[i].average_overall < overall[1] && results[i].average_overall > overall[0])) {
            match++;
            $(".results").append('<li class="list-group-item course clearfix">' +
                '<div class="details col-xs-12 col-sm-4">' +
                '<a href="/summary/course/' + results[i].course_id + '/" class="courselink">' + results[i].course_code + ': ' +
                results[i].course_name + '</a><br/>' +
                results[i].lecturer + '<br/>' +
                '<a href="/summary/uni/' + results[i].uni_id + '" class="unilink">' + results[i].uni + '</a>' +
                '</div>' +
                '<div class="col-sm-8 clearfix">' + ((results[i].average_overall == null) ? "<div class=\"norating col-xs-12\">No Ratings" : "<div class=\"ratinggroup\"><div class=\"col-sm-6 col-lg-4\">Overall Rating" +
                ": " + results[i].average_overall + "</div><div class=\"col-sm-6 col-lg-4\">Materials Rating: " + results[i].average_materials + "</div><div class=\"col-sm-6 col-lg-4\">" +
                "Difficulty Rating: " + results[i].average_difficulty + "</div><div class=\"col-sm-6 col-lg-4\">Teaching Rating: " + results[i].average_teaching + "</div>" +
                "<div class=\"col-sm-6 col-lg-4\">Satisfaction Rating: " + results[i].average_satisfaction + "</div>") + '</div>' +
                '</li>');
        }
    }

    if (match === 0) {
        $(".results").append("<li class='list-group-item noresults clearfix'>No results found.</li>")

        return;
    }
}

function createUniChecks() {
    unis = [];
    for (var i = 0; i < results.length; i++) {
        if (unis.indexOf(results[i].uni) == -1) {
            unis.push(results[i].uni);
        }
    }
    if (unis.length > 1) {
        for (var i = 0; i < unis.length; i++) {
            $("#uniCheckList").append("<input type=\"checkbox\" class=\"unichk\" id=\"" + unis[i] + "\"><label for=\"" + unis[i] + "\">" + unis[i] + "</label><br>")
        }
        $("#uniCheck").removeClass("hidden");
    }
}
function createLecturerChecks() {
    unis = [];
    for (var i = 0; i < results.length; i++) {
        if (unis.indexOf(results[i].lecturer) == -1) {
            unis.push(results[i].lecturer);
        }
    }
    if (unis.length > 1) {
        for (var i = 0; i < unis.length; i++) {
            $("#lecCheckList").append("<input type=\"checkbox\" class=\"lecchk\" id=\"" + unis[i] + "\"><label for=\"" + unis[i] + "\">" + unis[i] + "</label><br>")
        }
        $("#lecCheck").removeClass("hidden");
    }
}


$(document).ready(function () {


    $.get("/api/results/" + GetURLParameter("s").replace("+", "_"), function (data) {
        results = data;
        createUniChecks();
        createLecturerChecks();

        $(".lecchk").each(function () {
            $(this).change(function () {
                if ($(this).prop("checked")) {
                    lec.push($(this).attr("id"));
                }
                else {
                    lec.splice($.inArray($(this).attr("id"), uni), 1);
                }
                loadResults();
            });
        });
        $(".unichk").each(function () {
            $(this).change(function () {
                if ($(this).prop("checked")) {
                    uni.push($(this).attr("id"));
                }
                else {
                    uni.splice($.inArray($(this).attr("id"), uni), 1);
                }
                loadResults();
            });
        });


        loadResults();
    });

    $("#asc").click(function () {
        asc = "Ascending";
        loadResults();
    });
    $("#desc").click(function () {
        asc = "Descending";
        loadResults();
    });

    $("#lecreset").click(function () {
        $(".lecchk").each(function () {
            $(this).prop("checked", false);
        });
        lec = [];
        loadResults();
    });
    $("#unireset").click(function () {
        $(".unichk").each(function () {
            $(this).prop("checked", false);
        });
        lec = [];
        loadResults();
    });

    $(".dropdown-menu li a").click(function () {
        var txt = $(this).text();
        $(this).closest(".btn-group").children().first().val($(this).text());
        $(this).closest(".btn-group").children().first().text($(this).text().split(" Rating")[0]);
        $(this).closest(".btn-group").children().first().append('   <span class="caret"></span>');
        loadResults();
    });

    $( "#slider-range-overall" ).slider({
      range: true,
      min: 0,
      max: 100,
      values: [ 0, 100 ],
      slide: function( event, ui ) {
          overall=[ui.values[0], ui.values[1]];
        $( "#amount-overall" ).val (ui.values[ 0 ] + " - " + ui.values[ 1 ] );
          loadResults();
      }
    });
    $( "#amount-overall" ).val( $( "#slider-range-overall" ).slider( "values", 0 ) +
      " - " + $( "#slider-range-overall" ).slider( "values", 1 ) );


})
;