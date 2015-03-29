Speeches.SpeechesController = function(){
	var that = {};

	var speechesModel = null;
	var speechesDistributionView = null;
	var speechesLineView = null;

	var init = function(){
		speechesModel = Speeches.SpeechesModel();
		speechesDistributionView = Speeches.SpeechesDistributionView();
		speechesLineView = Speeches.SpeechesLineView();
		initGoogleCharts();

		initListener();

		speechesModel.init();
	};

	var initListener = function(){
		$(speechesModel).on("InfoFinished", visu);
	};

	var visu = function(){
		var scenesInfo = speechesModel.getScenesInfo();
		speechesDistributionView.render(scenesInfo);

		var distribution = speechesModel.getDistribution();
		speechesLineView.render(distribution);
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