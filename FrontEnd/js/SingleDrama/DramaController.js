SingleDrama.DramaController = function(){
	var that = {};

	var dramaModel = null;
	var tableDramaView = null;
	var barChartDramaView = null;

	var init = function(){

		dramaModel = SingleDrama.DramaModel();
		tableDramaView = SingleDrama.TableDramaView();
		barChartDramaView = SingleDrama.BarChartDramaView();

		dramaModel.init();
		barChartDramaView.init();
		initGoogleCharts();

		initListener();

	};

	var initGoogleCharts = function(){
		// Load the Visualization API and the piechart package.
      	setTimeout(function(){google.load('visualization', '1', {'callback': doNothing, 
      		'packages':['corechart']})}, 0);
	};

	var doNothing = function(){

	};

	var initListener = function(){
		$(dramaModel).on("ActsInfoFinished", visu);
		$(barChartDramaView).on("ActSelectionClicked", visuActBarChart);
	};

	var visu = function(event){
		var actInfo = dramaModel.getActInfo();
		barChartDramaView.setActSelection();
		tableDramaView.renderAct(actInfo);
		barChartDramaView.drawChartAct(actInfo);
	};

	var visuActBarChart = function(event){
		var actInfo = dramaModel.getActInfo();
		barChartDramaView.setActSelection();
		barChartDramaView.drawChartAct(actInfo);
	};

	that.init = init;

	return that;
};