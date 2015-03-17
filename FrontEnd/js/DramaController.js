DramaAnalyzer.DramaController = function(){
	var that = {};

	var dramaModel = null;
	var dramaListView =null;

	var init = function(){
		dramaModel = DramaAnalyzer.DramaModel();
		dramaModel.init();

		dramaListView = DramaAnalyzer.DramaListView();
		dramaListView.init();

		initListener();

		console.log("start Retrieval");
		dramaModel.retrieveAllData();
	};

	var initListener = function(){
		$(dramaModel).on("AllDataRetrieved", updateList);
	};

	var updateList = function(event, dramaList){
		dramaListView.renderList(dramaList);
	};

	that.init = init;

	return that;
};