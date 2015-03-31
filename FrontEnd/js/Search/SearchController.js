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
		$(dramaListView).on("DramaClicked", analyzeDrama);
	};

	var analyzeDrama = function(event, drama_id, title, author){
		dramaListModel.saveCurrentDrama(drama_id, title, author);
		//Probably not working in every browser
		window.open("drama.html", "_blank");
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