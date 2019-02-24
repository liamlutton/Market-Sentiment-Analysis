var dataGlobal;
var dataPointsUsed = [];

var socket = io();

function getJSON(company) {
    socket.emit('request-stock', 'eBay');

    path = "assets/js/data/" + company + ".json";

    // Do something
    $.getJSON(path, function(json) {
        dataGlobal = json; // this will show the info it in firebug console
    });

}

//getJSON();



function displayData(comanyName, stockGeneral, positiveId, negativeID) {
    getJSON(comanyName);

    setTimeout(function(){
        //do what you need here

        displayEmotions(stockGeneral, positiveId, negativeID);

      }, 500);
}

function displayEmotions(documentId, positiveDocId, negativeDocId) {

    output = "";

    //output ="";

    //output = "Emotions:<br>";

    dictionary = dataGlobal.emotions;


    for (var key in dictionary) {
        // check if the property/key is defined in the object itself, not in parent
        if (dictionary.hasOwnProperty(key)) {

            /**
            dataPointsUsed.push({
                key:   "y",
                value: dictionary[key],
                key:   "label",
                value: key
                });*/

                dataPointsUsed.push({y: dictionary[key], label: key});


            if (dictionary[key] > 18) {
                color = "lightgreen;";
            } else {
                color = "red;";
            }
            output += '<li>' + key + '<span><i class=""></i>' + dictionary[key] + '</span></li>' ;
        }
    }


    document.getElementById(documentId).innerHTML += output;

    //display the positive emotion card
    positiveOutput = dataGlobal.percentPositive;

    document.getElementById(positiveDocId).innerHTML = positiveOutput;

    //display the negative emotion card
    negativeOutput = dataGlobal.percentNegative;

    document.getElementById(negativeDocId).innerHTML = negativeOutput;

    var chart = new CanvasJS.Chart("chartContainer", {
        animationEnabled: true,
        title: {
            text: "Emotional Breakdown from Recent Media"
        },
        data: [{
            type: "pie",
            startAngle: 240,
            yValueFormatString: "##0.00\"%\"",
            indexLabel: "{label} {y}",
            dataPoints: dataPointsUsed

        }]
    });
    chart.render();
}
