MultipleDramas.MultipleDramasController = function(){
	var that = {};

	var multipleDramasModel = null;
	var yearView = null;


	var init = function(){

		multipleDramasModel = MultipleDramas.MultipleDramasModel();
		yearView = MultipleDramas.YearView();

		multipleDramasModel.init();

		initGoogleCharts();

		initListener();

	};

	var initListener = function(){
		$(multipleDramasModel).on("InfoFinished", visu);
	};

	var visu = function(){
		var dramas = multipleDramasModel.getChosenDramas();
		yearView.renderScatterChart(dramas);
	};

	var initGoogleCharts = function(){
		// Load the Visualization API and the piechart package.
      	setTimeout(function(){google.load('visualization', '1', {'callback': doNothing, 
      		'packages':['corechart', 'controls']})}, 0);
	};

	var doNothing = function(){
	};

	that.init = init;

	return that;
};