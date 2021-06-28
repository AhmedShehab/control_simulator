function run() {
	var btn = document.getElementById("descButton");
	var pdf = document.getElementById("pdf");
	if (btn.innerText == "Show System Description") {
		btn.innerHTML = "Hide System Description<span class='arrowDown'></span>";
		pdf.style.height = "100vh";
		scrollTo(0, 740);
	} else {
		btn.innerHTML = "Show System Description<span class='arrowUp'></span>";
		scrollTo(0, 0);
		setTimeout(() => {
			pdf.style.height = "0";
		}, 500);
	}
}
