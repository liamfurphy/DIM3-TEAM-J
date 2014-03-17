$(document).ready(function () {
    $("#submitbtn").click(function(){
        $.post('/api/course/'+$('#submitbtn').attr("val")+"/", $('#courseform').serialize())
        alert("Course added!");
    })
});