Speakers.SpeakerRelationsView = function(){
	var that = {};
	var currentSpeaker = "";

	var init = function(){
		initListener();
	};

	var initListener = function(){
		$("#selection-speaker-relations").change(speakersSelectionClicked);
	};

	var renderRelation = function(speakersInfo){
		var speaker = findSpeakerInSpeakersInfoByName(speakersInfo);
		$("#speaker-name").text(speaker.name);
		$("#gets-dominated-by").text(speaker.relations.gets_dominated_by);
		$("#alternative").text(speaker.relations.alternative);
		$("#concomitant").text(speaker.relations.concomitant);
		$("#independent").text(speaker.relations.independent);
	};

	var findSpeakerInSpeakersInfoByName = function(speakersInfo){
		for(var i = 0; i < speakersInfo.length; i++){
			if(speakersInfo[i].name == currentSpeaker){
				return speakersInfo[i];
			}
			
		}
	};

	var buildSelection = function(speakersInfo){
		$select = $("#selection-speaker-relations");
		for(var i = 0; i < speakersInfo.length; i++){
			var name = speakersInfo[i].name;
			var option = $("<option>");
			option.text(name);
			$select.append(option);
		}
	};

	var setCurrentSpeaker = function(){
		currentSpeaker = $("#selection-speaker-relations").val();
	};

	var speakersSelectionClicked = function(){
		$(that).trigger("SpeakerRelationsSelectionClicked");		
	};

	that.init = init;
	that.buildSelection = buildSelection;
	that.renderRelation = renderRelation;
	that.setCurrentSpeaker = setCurrentSpeaker;

	return that;
};