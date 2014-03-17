var since;
$(document).ready(function () {


    $.get("/api/latest/", function (data) {
        parse_data(data);});
});


function loadSince() {
    $.get("/api/latest/" + since, function (data) {
        parse_data(data);
    });
}
function updateTicker(data) {
    $("#ticker-form").append("            <ul id=\"js-news\" class=\"js-hidden\"></ul>");
    for(var i = 0; i< data.length; i++){
    var x = data[i];
    $("#js-news").prepend("<li class=\"ratingelem col-xs-12 col-md-6 col-lg-4\"><div>" + x.username + " rated " + x.classname + " " + x.score + "/10</div></li>");}

}

function parse_data(data) {
    if (data.length > 0) {
        since = data[0].datestr;
        updateTicker(data);
        updateticker();

    }
        window.setTimeout(loadSince, 15000);


}

function updateticker() {
    $(".ticker-wrapper").remove();
    $('#js-news').ticker({speed: 0.10,           // The speed of the reveal
        controls: false,        // Whether or not to show the jQuery News Ticker controls
        titleText: '',   // To remove the title set this to an empty String
        displayType: 'fade', // Animation type - current options are 'reveal' or 'fade'
        pauseOnItems: 3000,    // The pause on a news item before being replaced
        fadeInSpeed: 600,      // Speed of fade in animation
        fadeOutSpeed: 300  });
}