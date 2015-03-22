Search.FormsView = function(){
	var that = {};

	var init = function(){
		$("#search-button").on("click", setFormInput);
		setFormInput();
	};

	var setFormInput = function(){
		var input = {}

		var title = $("#input-title").val();
		var author = $("#input-author").val();
		var date_from = $("#input-date-from").val();
		var date_to = $("#input-date-to").val();

		if(title != ""){input["title"] = title;}
		if(author != ""){input["author"] = author;}

		var range = {}
		if(date_from != ""){range.from = parseInt(date_from);}
		if(date_to != ""){range.to = parseInt(date_to);}
		if(date_from != "" || date_to != ""){input["year"] = range;}

		$(that).trigger("InputCatched", [input]);
	};

	that.init = init;

	return that;
};