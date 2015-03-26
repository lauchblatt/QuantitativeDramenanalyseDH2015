Speakers.SpeakersController = function(){
	var that = {};

	var speakersModel = null;
	var speakersTableView = null;

	var init = function(){
		speakersModel = Speakers.SpeakersModel();
		speakersTableView = Speakers.SpeakersTableView();

		speakersModel.init();

		initListener();

	};

	var initListener = function(){
		$(speakersModel).on("InfoFinished", visu);
	};

	var visu = function(){
		var speakersInfo = speakersModel.getSpeakersInfo();
		speakersTableView.renderTable(speakersInfo);
	};

	that.init = init;

	return that;
};