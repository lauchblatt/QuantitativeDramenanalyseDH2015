MultipleDramas.MultipleDramasController = function(){
	var that = {};

	var multipleDramasModel = null;
	var yearView = null;


	var init = function(){

		multipleDramasModel = MultipleDramas.MultipleDramasModel();
		yearView = MultipleDramas.YearView();

		multipleDramasModel.init();
		yearView.init();

		initGoogleCharts();

		initListener();

	};

	var initListener = function(){
		$(multipleDramasModel).on("InfoFinished", visu);
		$(yearView).on("YearSelectionClicked", visuYearChart);
	};

	var visu = function(){
		var dramas = multipleDramasModel.getChosenDramas();

		yearView.setYearSelection();
		yearView.renderScatterChart(dramas);
	};

	var visuYearChart = function(){
		var dramas = multipleDramasModel.getChosenDramas();
		yearView.setYearSelection();
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