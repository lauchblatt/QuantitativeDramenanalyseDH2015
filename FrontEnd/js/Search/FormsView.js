Search.FormsView = function(){
	var that = {};

	var init = function(){
		$("#search-button").on("click", setFormInput);
		$("body").on("keypress", function(event){
			var key = event.which || event.keyCode;
			if(key == 13){
				setFormInput();
			}
		});
		setFormInput();
	};

	var setFormInput = function(){
		var input = {}

		var title = $("#input-title").val();
		var author = $("#input-author").val();

		var isComedy = $("#check-comedy").is(":checked");
		var isTragedy = $("#check-tragedy").is(":checked");
		var isPageant = $("#check-pageant").is(":checked");

		var date_from = $("#input-date-from").val();
		var date_to = $("#input-date-to").val();
		var acts_from = $("#input-numberOfActs-from").val();
		var acts_to = $("#input-numberOfActs-to").val();
		var scenes_from = $("#input-numberOfScenes-from").val();
		var scenes_to = $("#input-numberOfScenes-to").val();
		var numberOfSpeeches_from = $("#input-numberOfSpeeches-from").val();
		var numberOfSpeeches_to = $("#input-numberOfSpeeches-to").val();

		if(title != ""){input["title"] = title;}
		if(author != ""){input["author"] = author;}

		input["isComedy"] = isComedy;
		input["isTragedy"] = isTragedy;
		input["isPageant"] = isPageant;

		var range = {};
		if(date_from != ""){range.from = parseInt(date_from);}
		if(date_to != ""){range.to = parseInt(date_to);}
		if(date_from != "" || date_to != ""){input["year"] = range;}

		var range = {};
		if(acts_from != ""){range.from = parseInt(acts_from);}
		if(acts_to != ""){range.to = parseInt(acts_to);}
		if(acts_from != "" || acts_to != ""){input["number_of_acts"] = range;}

		var range = {};
		if(scenes_from != ""){range.from = parseInt(scenes_from);}
		if(scenes_to != ""){range.to = parseInt(scenes_to);}
		if(scenes_from != "" || acts_to != ""){input["number_of_scenes"] = range;}

		var range = {};
		if(numberOfSpeeches_from != ""){range.from = parseInt(numberOfSpeeches_from);}
		if(numberOfSpeeches_to  != ""){range.to = parseInt(numberOfSpeeches_to);}
		if(numberOfSpeeches_from != "" || numberOfSpeeches_to  != ""){input["number_of_speeches_in_drama"] = range;}

		$(that).trigger("InputCatched", [input]);
	};

	that.init = init;

	return that;
};