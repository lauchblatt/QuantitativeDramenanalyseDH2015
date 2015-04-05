Speeches.SpeechesController = function(){
	var that = {};

	var speechesModel = null;
	var speechesDistributionView = null;
	var speechesLineView = null;

	var init = function(){
		speechesModel = Speeches.SpeechesModel();
		speechesDistributionView = Speeches.SpeechesDistributionView();
		speechesLineView = Speeches.SpeechesLineView();
		speechesLineView.init();
		initGoogleCharts();

		initListener();

		speechesModel.init();
	};

	var initListener = function(){
		$(speechesModel).on("InfoFinished", visu);
		$(speechesLineView).on("SelectionClicked", visuCurve);
	};

	var visuCurve = function(){
		speechesLineView.setSelection();
		var selection = speechesLineView.getSelection();
		var distribution = null;
		if(selection == "Absolut"){
			distribution = speechesModel.getDistribution();
			speechesLineView.renderAbsolute(distribution)
		}
		if(selection == "Relativ"){
			distribution = speechesModel.getDistributionInPercent();
			speechesLineView.renderRelative(distribution)
		}

		
	};

	var visu = function(){
		var scenesInfo = speechesModel.getScenesInfo();
		speechesDistributionView.render(scenesInfo);

		var distribution = speechesModel.getDistributionInPercent();
		speechesLineView.renderRelative(distribution);

		$("#dramaTitle").text(localStorage["title"] + " (" + localStorage["year"] + ")");
		$("#dramaAuthor").text(localStorage["author"]);

		$(".container").fadeIn("slow");
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