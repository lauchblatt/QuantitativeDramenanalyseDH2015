SA_Relations.RelationsController = function(){
	var that = {};

	var relationsModel = null;
	var dramaView = null;

	var init = function(){
		relationsModel = SA_Relations.RelationsModel();
		dramaView = SA_Relations.RelationsDramaView();
		initGoogleCharts();
	};

	//Workaround to get Google Charts working
	var initGoogleCharts = function(){
		// Load the Visualization API and the piechart package.
      	setTimeout(function(){google.load('visualization', '1', {'callback': continueInit, 
      		'packages':['corechart', 'controls']})}, 0);
	};

	var continueInit = function(){
		relationsModel.init();
		var dramaRelationsMetrics = relationsModel.getDramaRelationsMetrics();

		dramaView.init(dramaRelationsMetrics);

	};

	that.init = init;

	return that;
};