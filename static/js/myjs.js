$(function(){
	console.log("Jquery Working");
	var list = {};
	var counter = 0;
	var valid_title = []; //thesis validation
	var input_title;	  //thesis validation

	function onFormSubmit(event) {

		var data = $(event.target).serializeArray();
		var thesis_data = {};

		//---------------for thesis validation----------------------//
		for (i = 0; i<counter; i++) {
			input_title = data[0].value;
			if (input_title.toLowerCase() == valid_title[i].toLowerCase())
			{
				alert("Already Input that thesis!");
				return false;
			}
		}
		//---------------for thesis validation----------------------//

		for (var i = 0; i < data.length; i++) {
			var key = data[i].name;
			var value = data[i].value;
			thesis_data[key] = value; 
		}

		var thesis_create_api = '/api/handler';
		$.post(thesis_create_api, thesis_data, function(response)
		{
			if (response.status = 'OK')
			{
				var full_data = response.data.yearlist + " " + response.data.thesis_title;
				$('ul.thesis-list').prepend('<li>'+full_data+' <a class="mybtn" href=\'thesis/edit/'+response.data.self_id+'\'>Edit</a><a class=\'mybtn\' href=\'thesis/delete/'+response.data.self_id+'\'>delete</a></li>');
				valid_title[counter] = response.data.thesis_title; //thesis validation
				counter+=1;										   //thesis validation
				$('form#form1 input[type=text], textarea').val("");
				$('form#form1 input[type=textarea], textarea').val("");
			}
			else alert('Error 192.168.1.10, Database error');
		})
		
		return false;
	}

	$('form#form1').submit(onFormSubmit);
	loadAllThesis();

	$(document).on('click', '.mybtn',function(){
		$(this).closest('li').remove();
	});

	function loadAllThesis() 
	{
		var thesis_list_api = '/api/handler';
		$.get(thesis_list_api,{},function(response){
			response.data.forEach(function(thesis) {
				var thesis_info = thesis.yearlist + " " + thesis.thesis_title;
				$('ul.thesis-list').append('<li>'+thesis_info+' <a class="mybtn" href=\'thesis/edit/'+thesis.self_id+'\'>Edit</a><a class=\'mybtn\' href=\'thesis/delete/'+thesis.self_id+'\'>delete</a></li>');
				valid_title[counter] = thesis.thesis_title;   //thesis validation
				counter+=1;									  //thesis validation
				return false;		
			})
		})
	}
	
});