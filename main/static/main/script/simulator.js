function run() {
	var btn = document.getElementById("descButton");
	var pdf = document.getElementById("pdf");
	if (btn.innerText == "Show System Description") {
		btn.innerHTML = "Hide System Description<span class='arrowDown'></span>";
		pdf.style.height = "100vh";
		var body = document.body,
			html = document.documentElement;
		var height = Math.max(body.scrollHeight, body.offsetHeight, html.clientHeight, html.scrollHeight, html.offsetHeight);
		scrollTo(0, height * 0.4679);
	} else {
		btn.innerHTML = "Show System Description<span class='arrowUp'></span>";
		scrollTo(0, 0);
		setTimeout(() => {
			pdf.style.height = "0";
		}, 500);
	}
	if (pdf.src == 'about:servo')
	{
		pdf.src="https://cloudpdf.io/document/f85e498d-8145-49e2-a385-ba08660ba4e4"	
	}
}
