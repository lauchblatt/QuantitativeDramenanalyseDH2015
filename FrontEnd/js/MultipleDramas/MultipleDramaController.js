MultipleDramas.MultipleDramasController = function(){
	var that = {};

	var multipleDramasModel = null;
	var yearView = null;
	var authorView = null;
	var categoryView = null;
	var lineCurveView = null;


	var init = function(){

		multipleDramasModel = MultipleDramas.MultipleDramasModel();
		yearView = MultipleDramas.YearView();
		authorView = MultipleDramas.AuthorView();
		categoryView = MultipleDramas.CategoryView();
		lineCurveView = MultipleDramas.LineCurveView();

		multipleDramasModel.init();
		yearView.init();
		authorView.init();
		categoryView.init();

		initGoogleCharts();

		initListener();

	};

	var initListener = function(){
		$(multipleDramasModel).on("InfoFinished", visu);
		$(yearView).on("YearSelectionClicked", visuYearChart);
		$(yearView).on("YearSelectionCompareClicked", visuYearChart);
		$(authorView).on("AuthorSelectionClicked", visuAuthorChart);
		$(categoryView).on("CategorySelectionClicked", visuCategoryChart);
	};

	var visu = function(){
		var dramas = multipleDramasModel.getChosenDramas();
		var authorList = multipleDramasModel.getAuthorList();
		var categoryList = multipleDramasModel.getCategoryList();
		var distribution = multipleDramasModel.getDistribution();
		var catDistribution = multipleDramasModel.getCategoryDistribution();
		var authorDistribution = multipleDramasModel.getAuthorDistribution();

		yearView.setYearSelection();
		yearView.setYearCompareSelection();
		yearView.renderScatterChart(dramas, authorList);
		
		authorView.setAuthorSelection();
		authorView.renderBarChart(authorList);
		
		categoryView.setCategorySelection();
		categoryView.renderColumnChart(categoryList);

		lineCurveView.render(distribution);

		$("body").fadeIn();

	};

	var visuCategoryChart = function(){
		var categoryList = multipleDramasModel.getCategoryList();
		categoryView.setCategorySelection();
		categoryView.renderColumnChart(categoryList);
	};

	var visuYearChart = function(){
		var dramas = multipleDramasModel.getChosenDramas();
		var authorList = multipleDramasModel.getAuthorList();

		yearView.setYearSelection();
		yearView.setYearCompareSelection();
		yearView.renderScatterChart(dramas, authorList);
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