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
		$(formsView).on("InputCatched", retrieveDramas);
	};

	var updateList = function(event, list){
		dramaListView.renderList(list);
	};

	var retrieveDramas = function(event, input){
		dramaListModel.retrieveDramas(input);
	};

	that.init = init;

	return that;
};