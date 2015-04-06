Drama.DramaView = function(){
	var that = {};
	var currentDrama_id = 0;

	var init = function(){
		initId();
		initLinks();
	};

	var initId = function(){
		var params = window.location.search
		currentDrama_id = (params.substring(params.indexOf("=") + 1));
	};

	var initLinks = function(){
		$("#to_matrix").attr("href", "matrix.html?drama_id=" + currentDrama_id);
		$("#to_dramaAnalysis").attr("href", "singledrama.html?drama_id=" + currentDrama_id);
		$("#to_speakerAnalysis").attr("href", "speakers.html?drama_id=" + currentDrama_id);
		$("#to_speechAnalysis").attr("href", "speeches.html?drama_id=" + currentDrama_id);
	};

	var renderView = function(dramaInfo){
		$("#dramaTitle").text(dramaInfo.title + " (" + dramaInfo.year + ")");
		$("#dramaAuthor").text(dramaInfo.author);
		$(".container").fadeIn("slow");
	};

	that.renderView = renderView;
	that.init = init;

	return that;
};