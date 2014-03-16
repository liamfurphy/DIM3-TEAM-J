var since;
$(document).ready(function () {

    $.get("/api/latest/", function (data) {
        parse_data(data);
    });
});


function loadSince() {
    $.get("/api/latest/" + since, function (data) {
        parse_data(data);
    });
}
function updateTicker(data) {
    var x = data[0];
    $("#ticker").prepend("<li class=\"ratingelem col-xs-12 col-md-6 col-lg-4\"><div>" + x.username + " rated " + x.classname +  " " + x.score + "</div></li>");
    if (data.length > 1) {
        window.setTimeout(function () {
            updateTicker(data.slice(1));
        }, 1000);
    }

}

function parse_data(data) {
    if (data.length > 0) {
        since = data[0].datestr;
        updateTicker(data);
    }
    window.setTimeout(loadSince, 1000);
}