var results;
var width;
var sort = 1;
var checked_unis = [];
var checked_lecturers = [];


cols = ["average_overall", "average_difficulty", "average_materials", "average_satisfaction", "average_teaching"];
column_details = {"average_overall": {"currentmin": 1, "currentmax": 10, "text": "Overall"},
    "average_difficulty": {"currentmin": 1, "currentmax": 10, "text": "Diffculty"},
    "average_materials": {"currentmin": 1, "currentmax": 10, "text": "Materials"},
    "average_satisfaction": {"currentmin": 1, "currentmax": 10, "text": "Satisfaction"},
    "average_teaching": {"currentmin": 1, "currentmax": 10, "text": "Teaching"}

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
    $(".results-container").addClass("col-md-8");

    if ($("#rating-sort").attr("value") !== null) {
        results.sort(function (a, b) {
            if (a.average_overall == null) {
                return (sort == 1) ? -1 : 1;
            }
            else if (b.average_overall == null) {
                return (sort == 1) ? 1 : -1;
            }
            var field = $("#rating-sort").attr("value");
            return (sort == 1) ? a[field] - b[field] : b[field] - a[field];

        });
    }

    $(".filters").removeClass("hidden");

    var match = 0;
    for (var i = 0; i < results.length; i++) {
        if ((checked_lecturers.length == 0 || checked_lecturers.indexOf(results[i].lecturer) != -1) && (checked_unis.length == 0 || checked_unis.indexOf(results[i].uni) != -1)) {
            var show = true;
            var nullshow = true;
            for (var key in results[i]) {


                if (cols.indexOf(key) == -1) continue; // Skip over the N values.
                var value = Number(results[i][key]);

                if (value < column_details[key].currentmin) {
                    show = false;
                }
                if (value > column_details[key].currentmax) {
                    show = false;
                }

                if ((show == false && value == 0 && (column_details[key].currentmin > 1 || column_details[key].currentmax < 10)) || value != 0) {
                    nullshow = false;
                }

            }


            if (show === true || nullshow == true) {
                match++;
                $(".results").append('<li class="list-group-item course clearfix">' +
                    '<div class="details col-xs-12 col-sm-4">' +
                    '<a href="/summary/course/' + results[i].course_id + '/" class="courselink">' + results[i].course_code + ': ' +
                    results[i].course_name + '</a><br/>' +
                    results[i].lecturer + '<br/>' +
                    '<a href="/summary/uni/' + results[i].uni_id + '" class="unilink">' + results[i].uni + '</a>' +
                    '</div>' +
                    '<div class="col-sm-8 clearfix">' + ((results[i].average_overall == 0) ? "<div class=\"norating col-xs-12\">No Ratings" : "<div class=\"ratinggroup\"><div class=\"col-sm-6 col-lg-4\">Overall Rating" +
                    ": " + results[i].average_overall + "</div><div class=\"col-sm-6 col-lg-4\">Materials Rating: " + results[i].average_materials + "</div><div class=\"col-sm-6 col-lg-4\">" +
                    "Difficulty Rating: " + results[i].average_difficulty + "</div><div class=\"col-sm-6 col-lg-4\">Teaching Rating: " + results[i].average_teaching + "</div>" +
                    "<div class=\"col-sm-6 col-lg-4\">Satisfaction Rating: " + results[i].average_satisfaction + "</div>") + '</div>' +
                    '</li>');
            }
        }
    }

    if (match === 0) {
        $(".results").append("<li class='list-group-item noresults clearfix'>No results found.</li>")

        return;
    }
}

function createChecks(attr, cid) {
    list = [];
    for (var i = 0; i < results.length; i++) {
        if (list.indexOf(results[i][attr]) == -1) {
            list.push(results[i][attr]);
        }
    }
    if (list.length > 1) {
        for (var i = 0; i < list.length; i++) {
            $("#" + cid + "CheckList").append("<input type=\"checkbox\" class=\"" + cid + "chk\" id=\"" + list[i] + "\"><label for=\"" + list[i] + "\">" + list[i] + "</label><br>")
        }
        $("#" + cid + "CheckSection").removeClass("hidden");
    }

}

$(document).ready(function () {

    width = $(window).width();
    if (width < 992) {
        $("#filterlist").collapse();
    }

    $.get(url, function (data) {
        results = data;
        createChecks("uni", "uni");
        createChecks("lecturer", "lec");

        $(".lecchk").each(function () {
            $(this).change(function () {
                if ($(this).prop("checked")) {
                    checked_lecturers.push($(this).attr("id"));
                }
                else {
                    checked_lecturers.splice($.inArray($(this).attr("id"), checked_unis), 1);
                }
                loadResults();
            });
        });
        $(".unichk").each(function () {
            $(this).change(function () {
                if ($(this).prop("checked")) {
                    checked_unis.push($(this).attr("id"));
                }
                else {
                    checked_unis.splice($.inArray($(this).attr("id"), checked_unis), 1);
                }
                loadResults();
            });
        });


        loadResults();
    });

    $("#asc").click(function () {
        sort = 1;
        loadResults();
    });
    $("#desc").click(function () {
        sort = 0;
        loadResults();
    });

    $("#lecreset").click(function () {
        $(".lecchk").each(function () {
            $(this).prop("checked", false);
        });
        checked_lecturers = [];
        loadResults();
    });

    $("#unireset").click(function () {
        $(".unichk").each(function () {
            $(this).prop("checked", false);
        });
        checked_unis = [];
        loadResults();
    });

    $(".dropdown-menu li a").click(function () {
        var txt = $(this).text();
        $(this).closest(".btn-group").children().first().val($(this).attr("val"));
        $(this).closest(".btn-group").children().first().text($(this).text().split(" Rating")[0]);
        $(this).closest(".btn-group").children().first().append('   <span class="caret"></span>');
        loadResults();
    });

    for (var i = 0; i < cols.length; i++) {
        var txt = cols[i];
        $('#sliders').append('<label class="field">' + column_details[txt]["text"] + ': </label><label type="text" class="pull-right" style="border:0; color:#428bca; font-weight:bold;"></label><div class="slider-range" id="' + txt + '"></div>');
    }

    /* Add the sliders to each slider element */
    $(".slider-range").each(function () {
        var current = $(this);
        current.slider({
            range: true,
            min: 1,
            max: 10,
            values: [1, 10],
            slide: function (event, ui) {
                column_details[current.attr('id')].currentmax = ui.values[1];
                column_details[current.attr('id')].currentmin = ui.values[0];
                setTimeout(function () {
                    current.prev().text(ui.values[ 0 ] + " - " + ui.values[ 1 ]);
                }, 15);
                loadResults();

            }
        });
        current.prev().text(current.slider("values", 0) + " - " + current.slider("values", 1));
    });

    $(window).resize(function () {
        if ($(window).width() < 992 && width >= 992) {
            $("#filterlist").collapse("hide");
        }
        else if ($(window).width() >= 992 && width < 992) {
            $("#filterlist").collapse("show");
        }
        width = $(window).width();
    });


})
;