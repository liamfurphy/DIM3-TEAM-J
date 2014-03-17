$(document).ready(function () {
    $("#submitbtn").click(function(){
        $.post('/api/rating/'+$('#submitbtn').attr("val")+"/", $('#ratingform').serialize())
        alert("Rating added!");
    })
});