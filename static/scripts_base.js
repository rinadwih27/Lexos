function havefiles() {
	var xhr = new XMLHttpRequest();

	var testURL = document.URL.split('/').slice(0, -1).join('/') + '/filesactive';

	alert(testURL);

	xhr.open("GET", testURL, false);
	xhr.setRequestHeader('testforactive', '');
	xhr.send();

	alert(xhr.responseText);

	if (xhr.responseText == 'True') {
		return true;
	}
	else {
		return false;
	}
}

$(function() {
	$("form").submit(function() {
		if (!havefiles()) {
			$("#submiterrormessage1").show().fadeOut(1200, "easeInOutCubic");
			return false;
		}
	});
});