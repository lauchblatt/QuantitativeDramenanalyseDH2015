Drama.DramaView = function(){
	var that = {};

	var init = function(){
		initButtons();
	};

	var renderView = function(dramaInfo){
		$("#title").text(dramaInfo.title + " (" + dramaInfo.year + ")");
		$("#author").text(dramaInfo.author);
		$(".container").fadeIn("slow");
	};

	var initButtons = function(){
		$("#configuration-matrix").on("click", toConfigMatrix);
		$("#drama-analysis").on("click", toDramaAnalyis);
		$("#speaker-analysis").on("click", toSpeakerAnalysis);
		$("#speeches-analysis").on("click", toSpeechesAnalysis);
	};

	var toConfigMatrix = function(){
		location.assign("matrix.html");
	};

	var toDramaAnalyis = function(){
		location.assign("singledrama.html");
	};

	var toSpeakerAnalysis = function(){
		location.assign("speakers.html");
	};

	var toSpeechesAnalysis = function(){
		location.assign("speeches.html");
	};

	that.renderView = renderView;
	that.init = init;

	return that;
};