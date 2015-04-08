Search.FormsView = function(){
	var that = {};

	var init = function(){
		$("#search-button").on("click", setFormInput);
		$("#more-button").on("click", showMoreRange);
		$("#less-button").on("click", showLessRange);
		$("body").on("keypress", function(event){
			var key = event.which || event.keyCode;
			if(key == 13){
				setFormInput();
			}
		});
		initTooltips();
		//setFormInput();
	};

	var initTooltips = function(){
		var tooltipOverall = $("#info-overall");
		tooltipOverall.tooltipster({
					content: 'Dieses Tool bietet Ihnen nicht nur die Möglichkeit,<br/> ein bestimmtes Drama quantitativ zu analysieren,<br/> sondern es ist auch möglich,<br/> mehrere Dramen miteinander zu vergleichen.',
					position: "right",
					trigger: 'hover',
					contentAsHTML: true
				});

		var tooltipOverall = $("#info-compare");
		tooltipOverall.tooltipster({
					content: 'Hiermit ist der Vergleich von mehreren Dramen möglich.<br/> Die mit einem Häkchen markierten Dramen befinden sich in der Sammlung.',
					position: "right",
					trigger: 'hover',
					contentAsHTML: true
				});

		var tooltipOverall = $("#input-author");
		tooltipOverall.tooltipster({
					content: 'z.B.: <i>Goethe</i> oder <i>Lessing Schiller Schlegel</i>',
					//content: '<i>z.B.:</i> Goethe <i>oder</i> Lessing Schiller Schlegel',
					position: "right",
					trigger: 'hover',
					contentAsHTML: true
				});
	};

	var showLessRange = function(){
		$("#more-button").fadeIn();
		$("#less-button").css("display", "none");
		$(".more-range").fadeOut();
	};

	var showMoreRange = function(){
		$("#more-button").css("display", "none");
		$("#less-button").fadeIn();
		$(".more-range").fadeIn();
	};

	var startLoadingAnimation = function(){
		$("#loading-text-button").text("Suche...");
		$("#loading-circle-button").css("display", "inline-block");
		$("#loading-spinner").css("display", "block");
	};

	var setFormInput = function(){
		startLoadingAnimation();
		var input = {}

		var title = $("#input-title").val();
		var author = $("#input-author").val();

		var isComedy = $("#check-comedy").is(":checked");
		var isTragedy = $("#check-tragedy").is(":checked");
		var isPageant = $("#check-pageant").is(":checked");

		var date_from = $("#input-date-from").val();
		var date_to = $("#input-date-to").val();
		var acts_from = $("#input-numberOfActs-from").val();
		var acts_to = $("#input-numberOfActs-to").val();
		var scenes_from = $("#input-numberOfScenes-from").val();
		var scenes_to = $("#input-numberOfScenes-to").val();
		var speakers_from = $("#input-numberOfSpeakers-from").val();
		var speakers_to = $("#input-numberOfSpeakers-to").val();
		var confDensity_from = $("#input-confDensity-from").val();
		var confDensity_to = $("#input-confDensity-to").val();
		var avg_from = $("#input-avgSpeechLength-from").val();
		var avg_to = $("#input-avgSpeechLength-to").val();
		var numberOfSpeeches_from = $("#input-numberOfSpeeches-from").val();
		var numberOfSpeeches_to = $("#input-numberOfSpeeches-to").val();

		if(title != ""){input["title"] = title;}
		if(author != ""){input["author"] = author;}

		input["isComedy"] = isComedy;
		input["isTragedy"] = isTragedy;
		input["isPageant"] = isPageant;

		var range = {};
		if(date_from != ""){range.from = parseInt(date_from);}
		if(date_to != ""){range.to = parseInt(date_to);}
		if(date_from != "" || date_to != ""){input["year"] = range;}

		var range = {};
		if(acts_from != ""){range.from = parseInt(acts_from);}
		if(acts_to != ""){range.to = parseInt(acts_to);}
		if(acts_from != "" || acts_to != ""){input["number_of_acts"] = range;}

		var range = {};
		if(scenes_from != ""){range.from = parseInt(scenes_from);}
		if(scenes_to != ""){range.to = parseInt(scenes_to);}
		if(scenes_from != "" || acts_to != ""){input["number_of_scenes"] = range;}

		var range = {};
		if(speakers_from != ""){range.from = parseInt(speakers_from);}
		if(speakers_to != ""){range.to = parseInt(speakers_to);}
		if(speakers_from != "" || speakers_to != ""){input["speaker_count"] = range;}

		var range = {};
		if(confDensity_from != ""){range.from = parseFloat(confDensity_from);}
		if(confDensity_to != ""){range.to = parseFloat(confDensity_to);}
		if(confDensity_from != "" || confDensity_to != ""){input["configuration_density"] = range;}

		var range = {};
		if(avg_from != ""){range.from = parseFloat(avg_from);}
		if(avg_to != ""){range.to = parseFloat(avg_to);}
		if(avg_from != "" || avg_to != ""){input["average_length_of_speeches_in_drama"] = range;}

		var range = {};
		if(numberOfSpeeches_from != ""){range.from = parseInt(numberOfSpeeches_from);}
		if(numberOfSpeeches_to  != ""){range.to = parseInt(numberOfSpeeches_to);}
		if(numberOfSpeeches_from != "" || numberOfSpeeches_to  != ""){input["number_of_speeches_in_drama"] = range;}

		$(that).trigger("InputCatched", [input]);
	};

	that.init = init;

	return that;
};