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
		$("#speaker-relation").css("display", "none");
		emptyRelations();
		var speaker = findSpeakerInSpeakersInfoByName(speakersInfo);
		setTextName(speaker.name);
		$("#gets-dominated-by").append(getList(speaker.relations.gets_dominated_by,
		 "Wird szenisch dominiert: "));
		$("#dominates").append(getList(speaker.relations.dominates,
		 "Dominiert: "));
		$("#alternative").append(getList(speaker.relations.alternative, 
			"Szenisch alternativ:"));
		$("#concomitant").append(getList(speaker.relations.concomitant, 
			"Szenisch konkomitant: "));
		$("#independent").append(getList(speaker.relations.independent, 
			"Szenisch unabhängig: "));
		$("#speaker-relation").fadeIn("slow");
	};

	var emptyRelations = function(){
		$("#gets-dominated-by").empty();
		$("#dominates").empty();
		$("#alternative").empty();
		$("#concomitant").empty();
		$("#independent").empty();
	}

	var getList = function(relations, headline){
		var text = $("<span>");
		var head = $("<b>" + headline + "</b>");
		var br = $("<br>");
		text.append(head);
		text.append(br);
		if(relations === undefined){
			var noSpeakers = $("<span>Keine Sprecher vorhanden</span>");
			text.append(noSpeakers);
			return text;
		}
		for(var i = 0; i < relations.length; i++){
			var oneSpeaker = $("<span>").text(relations[i]);
			oneSpeaker.append(br);
			text.append(oneSpeaker);
		}
		return text;
	};

	var setTextName = function(speakerName){
		var box = $("#speaker-name");
		box.text(speakerName);
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