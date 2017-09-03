SA_Relations.RelationsDramaView = function(){
	var that = {};

	var metricsForDramaRelations = {};
	var chosenTargets = [];


	var init = function(dramaRelationsMetrics){
		initListener();
		metricsForDramaRelations = dramaRelationsMetrics;
		console.log(metricsForDramaRelations);
		renderSpeakerDropDown();
		renderCheckboxes();

	};

	var initListener = function(){

		$("#selection-relationsDrama-metric").change(renderTargetsAndRelationsDrama);
		$("#selection-relationsDrama-normalisation").change(renderTargetsAndRelationsDrama);
		$("#selection-relationsDrama-speaker").change(renderTargetsAndRelationsDrama);

	};

	var renderTargetsAndRelationsDrama = function(){
		renderCheckboxes();
		renderRelationsDrama();
	};


	var setChosenTargets = function(){
		chosenTargets = [];
		var checkboxes = ($(".checkboxes-dramaRelations"));
		for(i = 0; i < checkboxes.length; i++){
			var isChecked = ($(checkboxes[i]).is(':checked'));
			if(isChecked){
				var target = $(checkboxes[i]).val();
				chosenTargets.push(target);
			}
		}
		console.log(chosenTargets);
	};

	var renderCheckboxes = function(){
		chosenSpeaker = $("#selection-relationsDrama-speaker").val();
		checkboxes = $("#checkboxes-dramaRelations");
		checkboxes.empty();
		var i = 0;
		for(var target in metricsForDramaRelations[chosenSpeaker]){
			if(i == 0){
				checkbox = $('<div class="checkbox"><label><input class="checkboxes-dramaRelations" checked type="checkbox" value="' + target + 
				'">' + target + '</label></div>');
			}else{
				checkbox = $('<div class="checkbox"><label><input class="checkboxes-dramaRelations" type="checkbox" value="' + target + 
				'">' + target + '</label></div>');
			}			
			i = i +1;
			checkbox.change(setChosenTargets);
			checkboxes.append(checkbox);
		}

	};

	var renderSpeakerDropDown = function(){
		var $speakerSelect = $("#selection-relationsDrama-speaker");
		for (var speaker in metricsForDramaRelations ){
			var $select = $("<option>" + speaker + "</option>");
			$speakerSelect.append($select);
		}	
	};


	var renderRelationsDrama = function(){
		var metricSelection = $("#selection-relationsDrama-metric").val();
		var normalisationSelection = $("#selection-relationsDrama-normalisation").val()
		var speakerSelection = $("#selection-relationsDrama-speaker").val()
		setChosenTargets();

		var metric = transformGermanMetric(metricSelection);
		var normalisation = transformGermanMetric(normalisationSelection);
		//var metrics = getRelationsActsMetrics(metric, normalisation, speakerSelection);
		//drawSpeakersActBarsChart(normalisationSelection, metricSelection, speakerSelection, metrics);
	};

	var getRelationsDramaMetrics = function(){

	};

	that.init = init;

	return that;
};