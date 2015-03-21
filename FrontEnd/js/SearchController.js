Search.SearchController = function(){
	var that = {};

	var dramaListModel = null;
	var dramaListView =null;
	var formsView = null;

	var init = function(){
		dramaListModel = Search.DramaListModel();
		dramaListModel.init();

		dramaListView = Search.DramaListView();
		dramaListView.init();

		formsView = Search.FormsView();
		formsView.init();

		initListener();
		/*
		console.log("start Retrieval");
		dramaListModel.retrieveAllData();
		*/
	};

	var initListener = function(){
		$(dramaListModel).on("AllDataRetrieved", updateList);
	};

	var updateList = function(event, dramaList){
		dramaListView.renderList(dramaList);
	};

	that.init = init;

	return that;
};