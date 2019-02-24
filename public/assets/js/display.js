var dataGlobal;

var dataPointsUsed = [];

var socket = io();

var globalCompanyName;

var globalNumArticles;

function getJSON(a) {
    path = "../../data.json";
    $.getJSON(path, function(a) {
        dataGlobal = a;
    });
}

function setNumArticles(a) {
    alert(a);
    globalNumArticles = a;
}

function getNumARticles() {}

function displayData(a, b, c, d, e) {
    getJSON(a);
    setTimeout(function() {
        displayEmotions(b, c, d, e);
    }, 100);
}

function displayEmotions(a, b, c, d) {
    output = "";
    dictionary = dataGlobal.emotions;
    for (var e in dictionary) if (dictionary.hasOwnProperty(e)) {
        dataPointsUsed.push({
            y: dictionary[e],
            label: e
        });
        if (dictionary[e] > 18) color = "lightgreen;"; else color = "red;";
        output += "<li>" + e + '<span><i class=""></i>' + dictionary[e] + "</span></li>";
    }
    document.getElementById(d).innerHTML = dataGlobal.companyName + " (" + dataGlobal.numberArticlesAnalyzed + " nodes back)";
    document.getElementById(a).innerHTML += output;

    positiveOutput = dataGlobal.percentPositive;
    document.getElementById(b).innerHTML = positiveOutput + "%";
    
    negativeOutput = dataGlobal.percentNegative;
    document.getElementById(c).innerHTML = negativeOutput + "%";

    var f = new CanvasJS.Chart("chartContainer", {
        animationEnabled: true,
        title: {
            text: ""
        },
        data: [ {
            type: "pie",
            startAngle: 240,
            yValueFormatString: '##0.00"%"',
            indexLabel: "{label} {y}",
            dataPoints: dataPointsUsed
        } ]
    });
    f.render();

}
