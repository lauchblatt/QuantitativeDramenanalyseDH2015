ActsScenes.ActsScenesController = function(){
	var that = {};

	var actsScenesModel = null;
	var actsScenesView = null;

	var init = function(){
		actsScenesModel = ActsScenes.ActsScenesModel();
		actsScenesView = ActsScenes.ActsScenesView();
		initGoogleCharts();
	};

	//Workaround to get Google Charts working
	var initGoogleCharts = function(){
		// Load the Visualization API and the piechart package.
      	setTimeout(function(){google.load('visualization', '1', {'callback': continueInit, 
      		'packages':['corechart']})}, 0);
	};

	var continueInit = function(){
		actsScenesModel.init();
		var metricsActs = actsScenesModel.getMetricsActs();
		actsScenesView.init(metricsActs);
		actsScenesView.render()
	};

	that.init = init;

	return that;
};