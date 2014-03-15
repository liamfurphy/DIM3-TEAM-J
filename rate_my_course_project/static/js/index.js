var since;
var slider = null;
$(document).ready(function () {

    $('.ratingbreakdown').each(function () {
        var num = $(this).attr("id").slice(6);
        $("#rating" + num).click(function () {
            $("#ratingpanel" + num).slideToggle();
        });
    });

    $.get("/api/latest/", function (data) {
        since = data[0].datestr;
        updateTicker(data);
        window.setTimeout(loadSince, 1000);
    });
});


function loadSince(){
$.get("/api/latest/"+since, function (data) {
    if(data.length>0){
    since = data[0].datestr;
        updateTicker(data);
         window.setTimeout(loadSince, 1000);
    }});
}
function updateTicker(data){
        var x = data[0];
        $("#ticker").prepend("<li class=\"ratingelem col-xs-12 col-md-6 col-lg-4\"><div>"+x.username+" rated " + x.classname +
        " "+ x.score+"</div></li>");
        if(data.length>1){
            window.setTimeout(function(){updateTicker(data.slice(1));}, 1000);
        }

}