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

		var date = {}
		if(date_from != ""){date["from"] = date_from;}
		if(date_to != ""){date["to"] = date_to;}
		if(date_from != "" || date_to != ""){input["date.when"] = date;}

		console.log(input);

		$(that).trigger("InputCatched", [input]);
	};

	that.init = init;

	return that;
};