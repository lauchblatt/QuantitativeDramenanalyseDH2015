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
		location.assign("matrix.html");
	};

	var toDramaAnalyis = function(){
		location.assign("singledrama.html");
	};

	var toSpeakerAnalysis = function(){
		location.assign("speakers.html");
	};

	that.renderView = renderView;
	that.init = init;

	return that;
};