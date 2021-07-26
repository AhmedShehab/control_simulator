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
function Reset(sys) {
	var simulator = document.title;
	var reset = document.getElementsByClassName("reset");
	var resetTime = document.getElementsByClassName("resetTime");
	var clear = document.getElementsByClassName("clear");
	var s,time;
	simulator == "Servomotor Simulator" ? (s = 90) : (s = 60);
	simulator == "Servomotor Simulator" ? (time = 15) : (time = 25);
	s = s.toFixed(1);
	time = time.toFixed(1)
	for (var i = 0; i < reset.length; i++) {
		reset[i].value = s;
	}
	for (var i = 0; i < resetTime.length; i++) {
		resetTime[i].value = time;
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
	// Wait 500 ms then load PDF when the page content is loaded
	setTimeout(() => {
		var pdf = document.getElementById("pdf");
		if (pdf.src == "about:servo") {
			pdf.src = "https://cloudpdf.io/document/f85e498d-8145-49e2-a385-ba08660ba4e4";
		} else {
			pdf.src = "https://cloudpdf.io/document/aad2b22a-7d7f-47e7-ac84-db6abc6f0b2e";
		}
	}, 500);

	// Calculate Step info and insert Values to the DOM
	var simulator = document.title;
	var p, i, d, zero, pole, gain, setPoint, sys;
	var selected = document.getElementsByTagName("select")[0].value;
	document.getElementsByName("setPoint").forEach((element) => {
		setPoint = element.value;
	});
	simulator == "Servomotor Simulator" ? (sys = "servo") : (sys = "cruise");
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
		fetch("/stepinfoapi/", {
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
				appendData(data);
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
		fetch("/stepinfoapi/", {
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
				appendData(data);
			});
	}
});

function appendData(data) {
	var div = document.querySelector("#calculating");
	document.querySelector("#removeCalculating").remove();
	var pRiseTime = document.createElement("p");
	var pOvershoot = document.createElement("p");
	var pSteadyStateValue = document.createElement("p");
	var pSteadyStateError = document.createElement("p");
	var pSettlingTime = document.createElement("p");
	var pPeak = document.createElement("p");
	var pPeakTime = document.createElement("p");
	data.SettlingTime == 0
		? (pSettlingTime.innerText = `Settling Time: Didn't reach 2% of the steady state`)
		: (pSettlingTime.innerText = `Settling Time: ${data.SettlingTime.toFixed(4)} seconds`);
	data.RiseTime <= 0
		? (pRiseTime.innerText = `Rise Time: Value didn't reach 90% of the steady state`)
		: (pRiseTime.innerText = `Rise Time: ${data.RiseTime.toFixed(4)} seconds`);
	pPeak.innerText = `Peak: ${data.Peak.toFixed(4)}`;
	pPeakTime.innerText = `Peak Time: ${data.PeakTime.toFixed(4)} seconds`;
	pOvershoot.innerText = `Percentage Overshoot: ${data.Overshoot.toFixed(4)} %`;
	pSteadyStateValue.innerText = `Steady State Value: ${data.SteadyStateValue.toFixed(4)}`;
	pSteadyStateError.innerText = `Steady State Error: ${data.SteadyStateError.toFixed(4)} %`;
	pSettlingTime.className = "removePadding";
	pOvershoot.className = "removePadding";
	pSteadyStateValue.className = "removePadding";
	pSteadyStateError.className = "removePadding";
	pRiseTime.className = "removePadding";
	pPeak.className = "removePadding";
	pPeakTime.className = "removePadding";
	div.append(pRiseTime);
	div.append(pSettlingTime);
	div.append(pPeak);
	div.append(pPeakTime);
	div.append(pOvershoot);
	div.append(pSteadyStateValue);
	div.append(pSteadyStateError);
}
