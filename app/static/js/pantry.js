$(document).ready(function() {
    $(document).keydown(function() {
	if (!$(":focus").is(":input")) {
	    $("#ean").focus();
	}
    });

    // Add a submit action to the Item Addition form
    $("#eanform").submit(function(event) {
	event.preventDefault();

	if ($("#ean").val().length < 6) return;

	var vals = {};
	$("#eanform :input").each(function(){vals[this.name]=$(this).val();});
	
	$.post($(this).attr('action'), vals)
	    .success(function(data) {
	      // it returns: {remaining, item: {upc, name, description, ingredient: {name, properties[], unit, provides[]}}}
	      var theItem = $("#ean-" + data.ean);

	      if (theItem && theItem.length) {
		  theItem.find(".remaining").text("Number remaining: " + (data.remaining));
	      } else {
		  theItem = list_added_pantry_item(data);
	      }

	      console.log(theItem);

	      if (data.item.ingredient == null) {
		  theItem.addClass("warning");
	      } else if (data.item.name == null) {
		  theItem.addClass("danger");
	      }

              $("#ean").val('');
	      $("#ean").focus();
	  }).error(function(err) {
	      console.error(err);
	      $("#ean").val('');
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

    $("#ean").focus();
});
