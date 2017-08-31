ActsScenes.ActsScenesController = function(){
	var that = {};

	var actsScenesModel = null;
	var actsScenesView = null;

	var init = function(){
		actsScenesModel = ActsScenes.ActsScenesModel();
		actsScenesView = ActsScenes.ActsScenesView();

		actsScenesModel.init();
		actsScenesView.init();
		initGoogleCharts();

		console.log("Hello World");

	};

	//Workaround to get Google Charts working
	var initGoogleCharts = function(){
		// Load the Visualization API and the piechart package.
      	setTimeout(function(){google.load('visualization', '1', {'callback': doNothing, 
      		'packages':['corechart']})}, 0);
	};

	var doNothing = function(){

	};

	that.init = init;

	return that;
};