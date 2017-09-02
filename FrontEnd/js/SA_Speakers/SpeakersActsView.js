SA_Speakers.SpeakersActsView = function(){
	var that = {};
	var metricsForSpeakerPerActs = {};


	var init = function(speakerActsMetrics){
		metricsForSpeakerPerActs = speakerActsMetrics;
		console.log(metricsForSpeakerPerActs);
		initListener();
		renderSpeakerDropDown();

	};

	var initListener = function(){
		$("#selection-speakersActs-bar-metric").change(renderSpeakersActBars);
		$("#selection-speakersActs-bar-normalisation").change(renderSpeakersActBars);
	};

	var renderSpeakerDropDown = function(){
		$speakerSelect = $("#selection-speakersActs-speaker-bar");
		for (var speaker in metricsForSpeakerPerActs){
			$select = $("<option>" + speaker + "</option>");
			$speakerSelect.append($select);
		}	
	};


	var renderSpeakersActBars = function(){
	};

	var drawSpeakersActBarsChart = function(){
	};

	that.init = init;

	return that;
};