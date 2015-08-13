$(function(){
	console.log("Jquery Working");
	var list = {};
	var counter = 0;
	var fname;
	var lname;
	function onFormSubmit(event) {

		var data = $(event.target).serializeArray();
		var student = {};
		
		for (i = 0; i<counter; i++) {
			fname = data[0].value;
			lname = data[1].value;
				if (list[i][0] != null) {
					if (fname.toLowerCase() == list[i][0].toLowerCase() && lname.toLowerCase() == list[i][1].toLowerCase()) {
					alert("Already Input that name!");
					return false;
				}
			}
		}

		console.log(data);
		for (var i = 0; i < data.length; i++) {
			var key = data[i].name;
			var value = data[i].value;
			student[key] = value; 
		}
		
		// var list_element = $('<li id="student'+counter+'">');


		

		// list_element.html(student.first_name + ' ' + student.last_name + ' ' + student.age + " <a class='mybtn' href='#'>delete</a></li>");
		// $('ul.student-list').prepend(list_element);
		// list[counter] = $('ul.student-list li').text().split(' ');
		// console.log(list[counter]);
		// counter +=1;
		// $('form#form1 input[type=text], textarea').val("");
		// $('form#form1 input[type=number], textarea').val("");

		var student_create_api = '/api/handler';
		$.post(student_create_api, student, function(response)
		{
			if (response.status = 'OK')
			{
				var full_data = response.data.yearlist + " " + response.data.thesis_title;
				console.log(full_data);
				$('ul.student-list').prepend('<li id="student'+counter+'">'+full_data+' <a class="mybtn" href=\'student/edit/'+student.self_id+'\'>Edit</a><a class=\'mybtn\' href=\'student/delete/'+student.self_id+'\'>delete</a></li>');
				list[counter] = $('ul.student-list li').text().split(' ');
				console.log(list[counter]);
				counter +=1;
				$('form#form1 input[type=text], textarea').val("");
				$('form#form1 input[type=textarea], textarea').val("");
			}
			else alert('Error 192.168.1.10, Database error');
		})
		
		return false;
	}

	$('form#form1').submit(onFormSubmit);
	
	$(document).on('click', '.mybtn',function(){
		$(this).closest('li').remove();
		var id_li = $(this).closest('li').attr('id');
		console.log(list[id_li.substr(7)]);
		list[id_li.substr(7)].splice(0,4);
	});


	function loadAllStudents() 
	{
		var student_list_api = '/api/handler';
		$.get(student_list_api,{},function(response){
			response.data.forEach(function(student) {
				var full_name = student.yearlist + " " + student.thesis_title;
				console.log("student id: "+student.self_id);
				$('ul.student-list').append('<li id="student'+counter+'">'+full_name+' <a class="mybtn" href=\'student/edit/'+student.self_id+'\'>Edit</a><a class=\'mybtn\' href=\'student/delete/'+student.self_id+'\'>delete</a></li>');
				list[counter] = $('ul.student-list li').text().split(' ');
				counter +=1;

				return false;
			})
		})
	}
	loadAllStudents();
	// var popular_movies_api = 'http://api.themoviedb.org/3/movie/popular';
	// $.get(popular_movies_api, {
	// 	api_key: 'cae620ff3f12488013dc1c9785960efe'
	// }, function(response) {
	// 	console.log('popular movies',response)
	// 	response.results.forEach(function(movie) {
	// 		$('ul.student-list').append('<li>' + movie.title + '</li>');
	// 	});
	// });


});