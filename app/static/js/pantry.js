$.ready(function() {
    // Add a submit action to the Item Addition form
    $("#eanform").submit(function(event) {
	event.preventDefault();

	var ean = $(this).find("input[name='ean']").val();
	var count = $(this).find("input[name='count']").val();
	var pantry = $(this).find("input[name='pk']").val();
	
	$.post($(this).attr('action'),
	   {"ean": ean, "count": count, "pk": pantry}
	  ).success(function(data) {
	      // it returns: {remaining, item: {upc, name, description, ingredient: {name, properties[], unit, provides[]}}}
	      var theItem = $("#ean" + data.itemean);

	      if (theItem.length) {
		  theItem.find(".remaining").text("Number remaining: " + (data.item.remaining));
	      } else {
		  theItem = list_added_pantry_item(data);
	      }

	      if (data.item.ingredient == null) {
		  theItem.addClass("warning");
	      } else if (data.item.name == null) {
		  theItem.addClass("danger");
	      }

	      console.log(data);
	  }).error(function(err) {
	      alert(err);
	  });;
	addToPantry(ean, count);
    });
});


function addToPantry(ean, count) {
}
