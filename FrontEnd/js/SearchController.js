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

		dramaListModel.retrieve();

	};

	var initListener = function(){
		$(dramaListModel).on("DataRetrieved", updateList);
		$(formsView).on("InputCatched", retrieveDramas);
	};

	var updateList = function(event, listItem){
		dramaListView.renderListItem(listItem);
	};

	var retrieveDramas = function(event, input){
		console.log(input);
	};

	that.init = init;

	return that;
};