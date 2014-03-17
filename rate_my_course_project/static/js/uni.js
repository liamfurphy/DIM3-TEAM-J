var courses;
var show = "average_overall";
google.load("visualization", "1", {packages: ["corechart"]});
google.setOnLoadCallback(googleDone);
function googleDone() {
    $(document).ready(function () {

        $(window).resize(function () {
            loadGraph();
        });

        $(".dropdown-menu li a").click(function () {
            show = $(this).attr("val");
            $(this).closest(".btn-group").children().first().text($(this).text());
            $(this).closest(".btn-group").children().first().append('   <span class="caret"></span>');
            loadGraph();
        });

        $.get("/api/courses/" + $("#statspanel").attr("val"), function (data) {
            courses = data;
            loadGraph();
        });
    });
}

function loadGraph() {
    var data = [
        ["Course", "Rating"]
    ];
    for (var i = 0; i < courses.length; i++) {
        data.push([courses[i].course_name, courses[i][show]]);
    }

    var data = google.visualization.arrayToDataTable(data);
    var options = {
        legend: { position: 'none' },
        histogram: { bucketSize: 1 }
    };

    var chart = new google.visualization.Histogram(document.getElementById('chart_div'));
    chart.draw(data, options);
}

