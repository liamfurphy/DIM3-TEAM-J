 var uni;
 var course;
 
 $(document).ready(function(){
	$(".uni" ).click(function(){
		
		uni = $(this).find("#uni_name").text();
		$(".uni").removeClass("light_blue");
		$("#final_list").fadeOut();
		$(this).addClass("light_blue");
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
				$(".course").removeClass("light_blue");
				$(this).addClass("light_blue");
				$.get('/get_course_instances/', {course:course, university:uni}, function(data){
					$("#final_list").html(data);
	   				$("#final_list").slideDown();
	   				
	   				
	   				$("#title_good").click(function(){
	   					$(".gcollapse").slideToggle();
	   					if ($("#gIcon").hasClass("glyphicon-chevron-down")){
	   						$("#gIcon").removeClass("glyphicon-chevron-down");
	   						$("#gIcon").addClass("glyphicon-chevron-up")
	   					}  	
	   					else{
	   						$("#gIcon").removeClass("glyphicon-chevron-up");
	   						$("#gIcon").addClass("glyphicon-chevron-down")
	   					}	   					
	   				});
	   				$("#title_bad").click(function(){
	   					$(".bcollapse").slideToggle();
	   					if ($("#bIcon").hasClass("glyphicon-chevron-down")){
	   						$("#bIcon").removeClass("glyphicon-chevron-down");
	   						$("#bIcon").addClass("glyphicon-chevron-up")
	   					}  	
	   					else{
	   						$("#bIcon").removeClass("glyphicon-chevron-up");
	   						$("#bIcon").addClass("glyphicon-chevron-down")
	   					}		   					
	   				});
	   				
	   				
				});
			});
			
	    });
    });
    $("#uni_header").click(function(){
		$("#uni_list").removeClass("hidden-xs");
	});
});



