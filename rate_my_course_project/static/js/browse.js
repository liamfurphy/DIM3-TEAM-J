 var uni;
 var course;
 
 $(document).ready(function(){
	$(".uni" ).click(function(){
		
		uni = $(this).find("#uni_name").text();
		$(".uni").removeClass("list-group-item-success");
		$("#final_list").fadeOut();
		$(this).addClass("list-group-item-success");
		$("#uni_list").addClass("hidden-xs");
		$.get('/get_uni_courses/', {university: uni}, function(data){
		
	   	 	$("#course_list").html(data);
	   		$("#course_list").slideDown();
	   		$(".course").click(function(){
	   			$("#c_list").addClass("hidden-xs");
	   			$("#course_header").click(function(){
					$("#c_list").removeClass("hidden-xs");
				});
				course = $(this).find("#course_name").text();
				$(".course").removeClass("list-group-item-success");
				$(this).addClass("list-group-item-success");
				$.get('/get_course_instances/', {course:course, university:uni}, function(data){
					$("#final_list").html(data);
	   				$("#final_list").slideDown();
	   				
	   				
	   				$(".title_good").click(function(){
	   					$(".gcollapse").slideToggle();	   					
	   				});
	   				$(".title_bad").click(function(){
	   					$(".bcollapse").slideToggle();	   					
	   				});
	   				
	   				
				});
			});
			
	    });
    });
    $("#uni_header").click(function(){
		$("#uni_list").removeClass("hidden-xs");
	});
});



