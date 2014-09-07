function list_added_pantry_item(item) {
    var outer = $("<div>", {"class": "list-group-item"});
    outer.append($("<h4>", {"class": "list-group-item-heading", "type": "button",
                            "data-toggle": "collapse", "data-target": "#ean-" + item.ean}).text("Name: " + item.name).append($("<a>", {"class": "deletebtn pull-right", "href": "#", "data-target": "#ean-" + item.ean}).append($("<span>", {"class": "glyphicon glyphicon-trash"}))));
    var inner = $("<div>", {"id": "ean-" + item.ean, "class": "collapse in"});
    outer.append(inner);
    if (item.remaining)
	inner.append($("<p>").addClass("remaining").append($("<span>", {"class": "remaining", "data-remaining": item.remaining}).text("Number remaining: ")));
    if (item.item.size)
	inner.append($("<p>").text("Size: " + item.item.size + " " + item.item.ingredient.unit));
    $("#pantry-items").prepend(outer);
    return outer;
}

function removeFromPantry(ean) {
    var ctr = $("#ean-" + ean + " .remaining");
    var pk = $("#ean-" + ean).data('pk');
    var remaining = ctr.data('remaining');
    remaining--;

    ctr.data('remaining', remaining);
    ctr.text(remaining);

    console.log(remaining);

    if (remaining == 0) {
	$.ajax({
	    "url": "/apy/v1/pantry-item/" + pk + "/",
	    "type": "DELETE",
	    "accepts": "application/json"
	}).success(function() {
	    $("#ean-" + ean).parent().remove();
	});
    } else {
	$.ajax({
	    "url": "/apy/v1/pantry-item/" + pk + "/",
	    "type": "PUT",
	    "accepts": "application/json",
	    "dataType": "json",
	    "processData": false,
	    "data": {
		"remaining": remaining
	    }
	});
    }
}

$(document).ready(function() {
    $(document).keydown(function() {
	if (!$(":focus").is(":input")) {
	    $("#ean").focus();
	}
    });

    $(".deletebtn").click(function(evt) {
	evt.preventDefault();
	evt.stopPropagation();
	removeFromPantry($(this).data('target').substr(5));
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
		  theItem.find(".remaining").text(data.remaining)
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
