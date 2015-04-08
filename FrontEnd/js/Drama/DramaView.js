Drama.DramaView = function(){
	var that = {};
	var currentDrama_id = 0;

	var init = function(){
		initId();
		initFields();
		initLinks();
	};

	var initId = function(){
		var params = window.location.search
		console.log("hello World");
		console.log(params);
		currentDrama_id = (params.substring(params.indexOf("=") + 1));
	};

	var initLinks = function(){
		$("#link-overall").attr("href", "drama.html?drama_id=" + currentDrama_id);
		$("#link-matrix").attr("href", "matrix.html?drama_id=" + currentDrama_id);
		$("#link-drama").attr("href", "singledrama.html?drama_id=" + currentDrama_id);
		$("#link-drama-actSceneAnalysis").attr("href", "singledrama.html?drama_id=" + currentDrama_id + "#act-scene-table");
		$("#link-drama-actStatistic").attr("href", "singledrama.html?drama_id=" + currentDrama_id + "#act-statistic");
		$("#link-drama-sceneStatistic").attr("href", "singledrama.html?drama_id=" + currentDrama_id + "#scene-statistic");
		$("#link-speakers").attr("href", "speakers.html?drama_id=" + currentDrama_id);
		$("#link-speaker-table").attr("href", "speakers.html?drama_id=" + currentDrama_id + "#speaker-table");
		$("#link-speeches-dominance").attr("href", "speakers.html?drama_id=" + currentDrama_id  + "#speeches-dominance");
		$("#link-speaker-statistic").attr("href", "speakers.html?drama_id=" + currentDrama_id  + "#speaker-statistic");
		$("#link-speaker-relations").attr("href", "speakers.html?drama_id=" + currentDrama_id  + "#speaker-relations");
		$("#link-speeches").attr("href", "speeches.html?drama_id=" + currentDrama_id);
		$("#link-histogram").attr("href", "speeches.html?drama_id=" + currentDrama_id + "#histogram");
		$("#link-curve-diagram").attr("href", "speeches.html?drama_id=" + currentDrama_id + "#curve-diagram");
	};

	var initFields = function(){
		$("#to_matrix").attr("href", "matrix.html?drama_id=" + currentDrama_id);
		$("#to_dramaAnalysis").attr("href", "singledrama.html?drama_id=" + currentDrama_id);
		$("#to_speakerAnalysis").attr("href", "speakers.html?drama_id=" + currentDrama_id);
		$("#to_speechAnalysis").attr("href", "speeches.html?drama_id=" + currentDrama_id);
	};

	var renderView = function(dramaInfo){
		$("#dramaTitle").text(dramaInfo.title + " (" + dramaInfo.year + ")");
		$("#dramaAuthor").text(dramaInfo.author);
		$(".container").fadeIn("slow");
		resizeOverviewBoxes();
	};

	var resizeOverviewBoxes = function(){
		$("#to_dramaAnalysis .box").height($("#to_matrix .box").height());
		$("#to_speechAnalysis .box").height($("#to_speakerAnalysis .box").height());
	};

	that.renderView = renderView;
	that.init = init;

	return that;
};