function generateRandomNumber(min, max, nachkommastellen) {
    return data[i]=(Math.random() * (max - min) + min).toFixed(nachkommastellen);
};


function generateFakeDataset(set_length){
    //var set_length = 10;

    var jumpstength = 10;   //Default: 10

    var current = 5;

    data = [set_length]
    for(i = 0; i < set_length;i++){
        //current+=generateRandomNumber(min,max,4);
        current+=(Math.floor(Math.random() * (jumpstength*3)-jumpstength))/10;
        data[i]=current;
    }


    console.log(data)
    return data;
}

function buildDataSet(name, data, filled, tension, color){      //Bsp.: buildDataSet("Temperatur",[1.0,1.2,1.6,1.9,2.4,2.9,3.4,3.3,3.8,4.5,6.0], true, 0.2,'rgba(56,105,225,0.5)')
    set = {
        label: name,
        fill: filled,
        lineTension: tension,
        backgroundColor: color,
        borderColor: color,
        data: data
    };
    console.log("Dataset successfully Build!")
    return set;
}

function buildGraph(canvasID, datasets, type, undertitles) {
    var chartObject = document.getElementById(canvasID).getContext("2d");

    if (type == "")
        type = "line";


    datasetlength = -100;
    for (i = 0; i < datasets.length; i++) {
        if (datasetlength == -100)
            datasetlength = datasets[i].data.length;
        if (datasets[i].data.length != datasetlength) {
            console.error("Alle übergebenen Datasets sollten gleich lang Sein!");
        }
    }

    //Using the first Datasets length, as reference for the Lenght of the whole Chart, they should all be the same size
    var data = datasets[0].data;

    //console.log(data)
    if(undertitles==null) {
        var buildLength = data.length;
        var currenCharUnderTitle = [buildLength]
        for (i = 0; i < buildLength; i++)
            currenCharUnderTitle[i] = "" + String(i + 1) + "";
    }else{
        var currenCharUnderTitle = undertitles;
    }

    var chart = new Chart(chartObject,
        {   type: type,
            data: {
                labels: currenCharUnderTitle,
                datasets: datasets
            },
            options: {
                title: {
                    display: true,
                    text: 'An/Aus Zeiten an bestimmten Tagen'
                },
                tooltips: {
                    mode: 'index',
                    intersect: false
                },
                responsive: true,
                scales: {
                    xAxes: [{
                        stacked: true,
                    }],
                    yAxes: [{
                        stacked: true
                    }]
                }
            }
        }
    );

}








if(false) {





    var graph_fill = false;
    var graph_swiftness = 0.2;
    var graph_alpha = 0.3;

//[0,1,3,4,4.3,4,3,2.4]   [1,2,2,4,4,5,6,6]
    var testset1 = buildDataSet("Einnahmen", generateFakeDataset(24), graph_fill,graph_swiftness,"rgba(56,105,225,"+graph_alpha+")");
    var testset2 = buildDataSet("Ausgaben", generateFakeDataset(24), graph_fill,graph_swiftness,"rgba(255,0,0,"+graph_alpha+")");
    var testset3 = buildDataSet("Zufall", generateFakeDataset(24), graph_fill,graph_swiftness,"rgba(0,255,0,"+graph_alpha+")");

    buildGraph("testChart", [testset3, testset2, testset1],"line");





//Settings

    /*

    lineTension: 0,
            radius: 5

     */


    var chart1 = document.getElementById("testChart").getContext("2d");


//data = [1.2,2.2,3.4,4.1,3.9,3.7,4.1,5.9,6.3,7.7]

    data1 = generateFakeDataset();
    data2 = generateFakeDataset();

    ta = [data.length]
    for (i = 0; i < data.length; i++)
        ta[i] = String(i);


    var chart = new Chart(chart1,
        {
            type: "line",
            data: {
                labels: ta,
                datasets: [
                    buildDataSet("Kühlung", data1, graph_fill, graph_swiftness, 'rgba(56,105,225,0.5)'),
                    {
                        label: "Explosivität",
                        fill: graph_fill,
                        lineTension: graph_swiftness,
                        backgroundColor: 'rgba(255,0,0,0.5)',
                        borderColor: 'rgba(255,0,0,0.5)',
                        data: data2
                    }
                ]
            },
            options: {
                animation: {
                    duration: 2000
                },
                scales: {
                    yAxes: [{ticks: {beginAtZero: true}}]
                }
            }
        }
    );


}