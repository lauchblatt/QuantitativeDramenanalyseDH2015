Search.FormsView = function(){
	var that = {};

	var init = function(){
		$("#search-button").on("click", getFormInput);
	};

	var getFormInput = function(){
		alert("waka waka"+ $("#input-title").val());
	};

	that.init = init;

	return that;
};