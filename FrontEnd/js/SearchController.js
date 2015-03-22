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

		initListener();
		formsView.init();

	};

	var initListener = function(){
		$(dramaListModel).on("DataRetrieved", updateList);
		$(dramaListModel).on("EmptyTable", emptyTable);
		$(formsView).on("InputCatched", retrieveDramas);
	};

	var updateList = function(event, listItem){
		dramaListView.renderListItem(listItem);
	};

	var retrieveDramas = function(event, input){
		dramaListModel.retrieveDramas(input);
	};

	var emptyTable = function(){
		dramaListView.emptyTable();
	}

	that.init = init;

	return that;
};