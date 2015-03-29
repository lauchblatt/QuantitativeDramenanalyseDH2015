Speakers.SpeakersController = function(){
	var that = {};

	var speakersModel = null;
	var speakersTableView = null;
	var speechesDominanceView = null;
	var speakersBarChartView = null;
	var speakerRelationsView = null;

	var init = function(){
		speakersModel = Speakers.SpeakersModel();
		speakersTableView = Speakers.SpeakersTableView();
		speechesDominanceView = Speakers.SpeechesDominanceView();
		speakersBarChartView = Speakers.SpeakersBarChartView();
		speakerRelationsView = Speakers.SpeakerRelationsView();

		speakersModel.init();
		speakersBarChartView.init();
		speakerRelationsView.init();
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
		$(speakersBarChartView).on("SpeakersSelectionClicked", visuBarChart);
		$(speakerRelationsView).on("SpeakerRelationsSelectionClicked", visuSpeakerRelations);
	};

	var visu = function(){
		var speakersInfo = speakersModel.getSpeakersInfo();

		speakersTableView.renderTable(speakersInfo);

		speechesDominanceView.renderPieChart(speakersInfo);

		speakersBarChartView.setSpeakersSelection();
		speakersBarChartView.renderBarChart(speakersInfo);

		speakerRelationsView.buildSelection(speakersInfo);
		speakerRelationsView.setCurrentSpeaker();
		speakerRelationsView.renderRelation(speakersInfo);

		$("body").fadeIn(1000);

	};

	var visuBarChart = function(){
		var speakersInfo = speakersModel.getSpeakersInfo();

		speakersBarChartView.setSpeakersSelection();
		speakersBarChartView.renderBarChart(speakersInfo);
	};

	var visuSpeakerRelations = function(){
		var speakersInfo = speakersModel.getSpeakersInfo();
		speakerRelationsView.setCurrentSpeaker();
		speakerRelationsView.renderRelation(speakersInfo);
	};

	that.init = init;

	return that;
};