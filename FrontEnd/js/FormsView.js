Search.FormsView = function(){
	var that = {};

	var init = function(){
		$("#search-button").on("click", setFormInput);
	};

	var setFormInput = function(){
		var input = {}
		input["title"] = $("#input-title").val();
		input["author"] = $("#input-author").val();
		$(that).trigger("InputCatched", [input]);
	};

	that.init = init;

	return that;
};