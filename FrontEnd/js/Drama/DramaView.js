Drama.DramaView = function(){
	var that = {};

	var init = function(){
		initButtons();
	};

	var renderView = function(dramaInfo){
		$("#title").text(dramaInfo.title);
		$("#author").text(dramaInfo.author);
	};

	var initButtons = function(){
		$("#configuration-matrix").on("click", toConfigMatrix);
		$("#drama-analysis").on("click", toDramaAnalyis);
		$("#speaker-analysis").on("click", toSpeakerAnalysis);
	};

	var toConfigMatrix = function(){
		location.replace("matrix.html");
	};

	var toDramaAnalyis = function(){
		location.replace("singledrama.html");
	};

	var toSpeakerAnalysis = function(){
		location.replace("speakers.html");
	};

	that.renderView = renderView;

	return that;
};