$(document).ready(function() {
    // Add a submit action to the Item Addition form
    $("#eanform").submit(function(event) {
	event.preventDefault();

	var vals = {};
	$("#eanform :input").each(function(){vals[this.name]=$(this).val();});
	
	$.post($(this).attr('action'), vals)
	    .success(function(data) {
		console.log(data);
	      // it returns: {remaining, item: {upc, name, description, ingredient: {name, properties[], unit, provides[]}}}
	      var theItem = $("#ean" + data.item.ean);

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
	  });
    });

    var eanInput = $("input[name='ean']");
    eanInput.autocomplete({
	"source": eanInput.data("autocomplete-url"),
	"minLength": 3,
	"select": function(evt, ui) {
	    $("#eapform").submit();
	}
    });
});
