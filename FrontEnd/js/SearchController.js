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

		console.log("start Retrieval");
		dramaListModel.retrieve();

	};

	var initListener = function(){
		$(dramaListModel).on("DataRetrieved", updateList);
	};

	var updateList = function(event, listItem){
		dramaListView.renderListItem(listItem);
	};

	that.init = init;

	return that;
};