$(document).ready(function () {
    $("#id_uni").change(function () {
        $.get("/api/get_lecturers/" + $('#id_uni').find(":selected").val(), function (data) {
            var self = $("#id_lecturer");
            self.empty();
            $.each(data, function (index, option) {
                $option = $("<option></option>").attr("value", -1).text(option[1]);
                self.append($option);
            });
            $("#id_lecturer").trigger("change");
        });
    });
    $("#id_lecturer").change(function () {
        if ($('#id_lecturer').find(":selected").text() === "New Lecturer") {
            $('<div class="input-group"><span class="input-group-addon">Lecturer Title</span><input class="form-control" id="id_lecturer_title" name="lecturer_title"type="text"></div><br>' +
'<div class="input-group"><span class="input-group-addon">Lecturer Name</span><input class="form-control" id="id_lecturer_name" name="lecturer_name"type="text"></div><br>' +
'<div class="input-group"><span class="input-group-addon">Lecturer Dept</span><input class="form-control" id="id_lecturer_dept" name="lecturer_dept"type="text"></div><br>' +
'<div class="input-group"><span class="input-group-addon">Lecturer Email</span><input class="form-control" id="id_lecturer_email" name="lecturer_email"type="text"></div><br>').insertBefore($('#id_description').parent());
        }
        else {
            ($("#id_lecturer_title").parent()).nextUntil("div:has(#id_description)").andSelf().remove();
        }
    });
});
