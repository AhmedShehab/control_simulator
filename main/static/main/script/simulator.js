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
	if (pdf.src == "about:servo") {
		pdf.src = "https://cloudpdf.io/document/f85e498d-8145-49e2-a385-ba08660ba4e4";
	} else {
		pdf.src = "https://cloudpdf.io/document/aad2b22a-7d7f-47e7-ac84-db6abc6f0b2e";
	}
}
function display() {
	var name = document.getElementById("selector").value;
	var elements = document.getElementsByClassName("option");
	for (let i = 0; i < elements.length; i++) {
		var element = elements[i];
		if (element.id == name) {
			document.getElementById(name).style.display = "block";
		} else {
			element.style.display = "none";
		}
	}
}
function Reset() {
	var reset = document.getElementsByClassName("reset");
	var clear = document.getElementsByClassName("clear");
	var s = 1.0;
	s = s.toFixed(1);
	for (var i = 0; i < reset.length; i++) {
		reset[i].value = s;
	}
	for (var i = 0; i < clear.length; i++) {
		clear[i].value = "";
	}
}
function openStepInfo() {
	document.getElementById("stepInfo").style.display = "flex";
}
function closeStepInfo() {
	document.getElementById("stepInfo").style.display = "none";
}

addEventListener("DOMContentLoaded", () => {
	var simulator = document.title;
	var p, i, d, zero, pole, gain, setPoint;
	var selected = document.getElementsByTagName("select")[0].value;
	document.getElementsByName("setPoint").forEach((element) => {
		setPoint = element.value;
	});
	if (simulator == "Servomotor Simulator") {
		var sys = "servo";
	} else {
		var sys = "cruise";
	}
	if (selected == "P" || selected == "PI" || selected == "PID" || selected == "PD") {
		document.getElementsByName("p").forEach((element) => {
			p = element.value;
		});
		document.getElementsByName("i").forEach((element) => {
			i = element.value;
		});
		document.getElementsByName("d").forEach((element) => {
			d = element.value;
		});
		fetch("/simulatorapi/", {
			method: "POST",
			body: JSON.stringify({
				sys: sys,
				p: p,
				i: i,
				d: d,
				setPoint: setPoint,
			}),
		})
			.then((response) => response.json())
			.then((data) => {
				var div = document.querySelector("#calculating");
				document.querySelector("#removeCalculating").remove();
				var pRiseTime = document.createElement("p");
				var pOvershoot = document.createElement("p");
				var pSteadyStateValue = document.createElement("p");
				var pSettlingTime = document.createElement("p");
				pRiseTime.innerText = `Rise Time: ${data.RiseTime.toFixed(4)} seconds`;
				pSettlingTime.innerText = `Settling Time: ${data.SettlingTime.toFixed(4)} seconds`;
				pOvershoot.innerText = `Percentage Overshoot: ${data.Overshoot.toFixed(4)} %`;
				pSteadyStateValue.innerText = `Steady State Value: ${data.SteadyStateValue.toFixed(4)}`;
				pSettlingTime.className = "removePadding";
				pOvershoot.className = "removePadding";
				pSteadyStateValue.className = "removePadding";
				pRiseTime.className = "removePadding";
				div.append(pRiseTime);
				div.append(pSettlingTime);
				div.append(pOvershoot);
				div.append(pSteadyStateValue);
			});
	} else {
		document.getElementsByName("zero").forEach((element) => {
			zero = element.value;
		});
		document.getElementsByName("pole").forEach((element) => {
			pole = element.value;
		});
		document.getElementsByName("gain").forEach((element) => {
			gain = element.value;
		});
		fetch("/simulatorapi/", {
			method: "POST",
			body: JSON.stringify({
				sys: sys,
				zero: zero,
				pole: pole,
				gain: gain,
				setPoint: setPoint,
			}),
		})
			.then((response) => response.json())
			.then((data) => {
				var div = document.querySelector("#calculating");
				document.querySelector("#removeCalculating").remove();
				var pRiseTime = document.createElement("p");
				var pOvershoot = document.createElement("p");
				var pSteadyStateValue = document.createElement("p");
				var pSettlingTime = document.createElement("p");
				pRiseTime.innerText = `Rise Time: ${data.RiseTime.toFixed(4)} seconds`;
				pSettlingTime.innerText = `Settling Time: ${data.SettlingTime.toFixed(4)} seconds`;
				pOvershoot.innerText = `Percentage Overshoot: ${data.Overshoot.toFixed(4)} %`;
				pSteadyStateValue.innerText = `Steady State Value: ${data.SteadyStateValue.toFixed(4)}`;
				pSettlingTime.className = "removePadding";
				pOvershoot.className = "removePadding";
				pSteadyStateValue.className = "removePadding";
				pRiseTime.className = "removePadding";
				div.append(pRiseTime);
				div.append(pSettlingTime);
				div.append(pOvershoot);
				div.append(pSteadyStateValue);
			});
	}
});
