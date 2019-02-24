var dataGlobal;

var dataPointsUsed = [];

var globalCompanyName;

var globalNumArticles = 0;

function getJSON(a) {
    path = "../../data.json";
    $.getJSON(path, function(a) {
        dataGlobal = a;
    });
}

function setNumArticles(a) {
    globalNumArticles = a;
}

function displayData(a, b, c, d, e, graphId) {
    getJSON(a);
    setTimeout(function() {
        displayEmotions(b, c, d, e, graphId);
    }, 100);
}

function displayEmotions(a, b, c, d, graphContainerId) {
    output = "";
    dictionary = dataGlobal.emotions;
    for (var e in dictionary) if (dictionary.hasOwnProperty(e)) {
        dataPointsUsed.push({
            y: dictionary[e],
            label: e
        });
        if (dictionary[e] > 18) color = "lightgreen;"; else color = "red;";
        output += "<li>" + e + '<span><i class=""></i>' + dictionary[e] + "%</span></li>";
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

    document.getElementById(graphContainerId).innerHTML = "<img src='public/assets/images/meanaverage.png'/>";
}
