$(document).ready(function () {
    $( "#id_uni" ).change(function() {
        $.get("/api/get_lecturers/" + $('#id_uni').find(":selected").val(), function (data) {
            var self = $("#id_lecturer");
            self.empty();
            $.each(data, function(index, option) {
                $option = $("<option></option>").attr("value", option[0]).text(option[1]);
                self.append($option);
            });
        });
    });
    $( "#id_lecturer" ).change(function() {
        if ($('#id_lecturer').find(":selected").val()==-1){
            $( "<br/>Lecturer name*: <input id=\"id_lecturer_name\" name=\"lecturer_name\" type=\"text\" />" ).insertAfter( $( '#id_lecturer' ) );
        }
    });
});