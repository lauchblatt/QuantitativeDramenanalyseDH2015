MultipleDramas.MultipleDramasController = function(){
	var that = {};

	var multipleDramasModel = null;
	var yearView = null;
	var authorView = null;


	var init = function(){

		multipleDramasModel = MultipleDramas.MultipleDramasModel();
		yearView = MultipleDramas.YearView();
		authorView = MultipleDramas.AuthorView();

		multipleDramasModel.init();
		yearView.init();
		authorView.init();

		initGoogleCharts();

		initListener();

	};

	var initListener = function(){
		$(multipleDramasModel).on("InfoFinished", visu);
		$(yearView).on("YearSelectionClicked", visuYearChart);
		$(authorView).on("AuthorSelectionClicked", visuAuthorChart);
	};

	var visu = function(){
		var dramas = multipleDramasModel.getChosenDramas();

		yearView.setYearSelection();
		yearView.renderScatterChart(dramas);

		var authorList = multipleDramasModel.getAuthorList();
		authorView.setAuthorSelection();
		authorView.renderBarChart(authorList);

		$("body").fadeIn();

	};

	var visuYearChart = function(){
		var dramas = multipleDramasModel.getChosenDramas();
		yearView.setYearSelection();
		yearView.renderScatterChart(dramas);
	};

	var visuAuthorChart = function(){
		var authorList = multipleDramasModel.getAuthorList();
		authorView.setAuthorSelection();
		authorView.renderBarChart(authorList);
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