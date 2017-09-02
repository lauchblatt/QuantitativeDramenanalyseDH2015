SA_Speakers.SA_SpeakersController = function(){
	var that = {};

	var speakersModel = null;
	var singleSpeakerView = null;
	var speakersComparisonView = null;

	var init = function(){
		speakersModel = SA_Speakers.SA_SpeakersModel();
		singleSpeakerView = SA_Speakers.SingleSpeakerView();
		speakersComparisonView = SA_Speakers.SpeakersComparisonView();
		initGoogleCharts();
	};

	//Workaround to get Google Charts working
	var initGoogleCharts = function(){
		// Load the Visualization API and the piechart package.
      	setTimeout(function(){google.load('visualization', '1', {'callback': continueInit, 
      		'packages':['corechart', 'controls']})}, 0);
	};

	var continueInit = function(){
		speakersModel.init();
		var dramaSpeakersProportions = speakersModel.getDramaSpeakersProportions();
		var actsSpeakersProportions = speakersModel.getActsSpeakersProportions();
		var scenesSpeakersProportions = speakersModel.getScenesSpeakersProportions();

		singleSpeakerView.init();
		singleSpeakerView.initSingleProportions(dramaSpeakersProportions, actsSpeakersProportions, scenesSpeakersProportions);
		singleSpeakerView.renderSpeakerPieChart();

		speakersComparisonView.init();
	};

	that.init = init;

	return that;
};