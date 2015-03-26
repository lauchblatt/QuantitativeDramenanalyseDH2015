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
		$(dramaModel).on("InfoFinished", visu);
		$(barChartDramaView).on("ActSelectionClicked", visuActBarChart);
		$(barChartDramaView).on("ScenesSelectionClicked", visuScenesBarCharts);
	};

	var visu = function(event){
		var actInfo = dramaModel.getActInfo();
		var scenesInfo = dramaModel.getScenesInfo();

		tableDramaView.renderAct(actInfo);

		barChartDramaView.setActSelection();
		barChartDramaView.drawChartAct(actInfo);

		barChartDramaView.setScenesSelection();
		barChartDramaView.drawChartScenes(scenesInfo);
	};

	var visuActBarChart = function(event){
		var actInfo = dramaModel.getActInfo();
		barChartDramaView.setActSelection();
		barChartDramaView.drawChartAct(actInfo);
	};

	var visuScenesBarCharts = function(event){
		var scenesInfo = dramaModel.getScenesInfo();
		barChartDramaView.setScenesSelection();
		barChartDramaView.drawChartScenes(scenesInfo);
	};

	that.init = init;

	return that;
};