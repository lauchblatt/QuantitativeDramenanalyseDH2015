SA_Relations.RelationsScenesView = function(){
	var that = {};

	var metricsForScenesRelations = {};
	var chosenTargets = [];
	var numberOfActs = -1;
	var numberOfScenes = -1;


	var init = function(actsRelationsMetrics, actsCount, scenesCount){
		initListener();
		metricsForScenesRelations = scenesRelationsMetrics;
		numberOfActs = actsCount;
		numberOfScenes = scenesCount;

		renderSpeakerDropDown();
		renderCheckboxes();

	};

	var initListener = function(){

		$("#selection-relationsActs-metric").change(renderRelationsScenes);
		$("#selection-relationsActs-normalisation").change(renderRelationsScenes);
		$("#selection-relationsActs-speaker").change(renderTargetsAndRelationsScenes);

	};

	var renderTargetsAndRelationsScenes = function(){
		renderCheckboxes();
		renderRelationsScenes();
	};


	var setChosenTargets = function(){
		chosenTargets = [];
		var checkboxes = ($(".checkboxes-scenesRelations"));
		for(i = 0; i < checkboxes.length; i++){
			var isChecked = ($(checkboxes[i]).is(':checked'));
			if(isChecked){
				var target = $(checkboxes[i]).val();
				chosenTargets.push(target);
			}
		}
	};

	var renderCheckboxes = function(){
		chosenSpeaker = $("#selection-relationsScenes-speaker").val();
		checkboxes = $("#checkboxes-scenesRelations");
		checkboxes.empty();
		for(var target in metricsForActsRelations[chosenSpeaker]){
			checkbox = $('<div class="checkbox"><label><input class="checkboxes-scenesRelations" checked type="checkbox" value="' + target + 
			'">' + target + '</label></div>');

			checkbox.change(renderRelationsScenes);
			checkboxes.append(checkbox);
		}

	};

	var renderSpeakerDropDown = function(){
		var $speakerSelect = $("#selection-relationsScenes-speaker");
		for (var speaker in metricsForScenesRelations ){
			var $select = $("<option>" + speaker + "</option>");
			$speakerSelect.append($select);
		}	
	};


	var renderRelationsScenes = function(){
		var metricSelection = $("#selection-relationsActs-metric").val();
		var normalisationSelection = $("#selection-relationsActs-normalisation").val()
		var speakerSelection = $("#selection-relationsActs-speaker").val()
		setChosenTargets();

		var metric = transformGermanMetric(metricSelection);
		var normalisation = transformGermanMetric(normalisationSelection);
		//var metrics = getRelationsActsMetrics(metric, normalisation, speakerSelection);

		//drawRelationsActsChart(metricSelection, normalisationSelection, speakerSelection, metrics);
	};

	var getRelationsScenesMetrics = function(metricName, typeName, speakerName){
	};

	var drawRelationsScenesChart = function(germanMetric, germanType, speakerName, metrics){

	};

	that.init = init;
	that.renderRelationsScenes = renderRelationsScenes;

	return that;
};