Speakers.SpeakersController = function(){
	var that = {};

	var speakersModel = null;
	var speakersTableView = null;
	var speechesDominanceView = null;

	var init = function(){
		speakersModel = Speakers.SpeakersModel();
		speakersTableView = Speakers.SpeakersTableView();
		speechesDominanceView = Speakers.SpeechesDominanceView();

		speakersModel.init();
		initGoogleCharts();

		initListener();

	};

	var initGoogleCharts = function(){
		// Load the Visualization API and the piechart package.
      	setTimeout(function(){google.load('visualization', '1', {'callback': doNothing, 
      		'packages':['corechart', 'controls']})}, 0);
	};

	var doNothing = function(){
	};

	var initListener = function(){
		$(speakersModel).on("InfoFinished", visu);
	};

	var visu = function(){
		var speakersInfo = speakersModel.getSpeakersInfo();
		speakersTableView.renderTable(speakersInfo);
		speechesDominanceView.renderPieChart(speakersInfo);

	};

	that.init = init;

	return that;
};