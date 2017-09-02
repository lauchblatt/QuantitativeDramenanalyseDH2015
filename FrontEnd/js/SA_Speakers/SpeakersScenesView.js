SA_Speakers.SpeakersScenesView = function(){
	var that = {};
	var metricsForSpeakerPerScenes = {};

	var init = function(speakerScenesMetrics){
		metricsForSpeakerPerScenes = speakerScenesMetrics;
		initListener();
		renderSpeakerDropDown();

	};

	var initListener = function(){
		$("#selection-speakerScenes-line-metric").change(renderSpeakersScenesLine);
		$("#selection-speakerScenes-line-type").change(renderSpeakersScenesLine);
		$("#selection-speakersScenes-speaker-line").change(renderSpeakersScenesLine);
	};

	var renderSpeakerDropDown = function(){
		var $speakerSelect = $("#selection-speakersScenes-speaker-line");
		for (var speaker in metricsForSpeakerPerScenes){
			var $select = $("<option>" + speaker + "</option>");
			$speakerSelect.append($select);
		}	
	};


	var renderSpeakersScenesLine = function(){
	};

	var drawSpeakersScenesLineChart = function(){

	};

	that.init = init;

	return that;
};