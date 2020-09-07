function addSymbols(e) {
    var suffixes = ["", "K", "M", "B"];
    var order = Math.max(Math.floor(Math.log(e.value) / Math.log(1000)), 0);

    if (order > suffixes.length - 1)
        order = suffixes.length - 1;

    var suffix = suffixes[order];
    return CanvasJS.formatNumber(e.value / Math.pow(1000, order)) + suffix;
}

function toggleDataSeries(e) {
    if (typeof(e.dataSeries.visible) === "undefined" || e.dataSeries.visible) {
        e.dataSeries.visible = false;
    } else {
        e.dataSeries.visible = true;
    }
    e.chart.render();
}

function plotgraph(title, data1, data2, id) {
    data_line = [];
    for (p of data1)
        data_line[data_line.length] = { x: new Date(p[0]), y: p[1] * 100 }
    data_bar = [];
    for (p of data2)
        data_bar[data_bar.length] = { x: new Date(p[0]), y: p[1] }
    console.log(data_bar);
    // console.log(dataPoints)
    var chart = new CanvasJS.Chart(id, {
        animationEnabled: true,
        theme: "light",
        zoomEnabled: true,
        panEnabled: true,
        dataPointMaxWidth: 20,
        title: {
            text: title
        },
        axisX: {
            title: "Date"
        },
        axisY: {
            title: "Sentiment",
            lineColor: "#C0504E",
            tickColor: "#C0504E",
            labelFontColor: "#C0504E",
            minimum: -100,
            maximum: 100,
        },
        axisY2: {
            title: "Volume",
            // suffix: "%",
            lineColor: "#4F81BC",
            tickColor: "#4F81BC",
            labelFontColor: "#4F81BC",

        },
        toolTip: {
            shared: true
        },
        legend: {
            cursor: "pointer",
            verticalAlign: "top",
            horizontalAlign: "center",
            dockInsidePlotArea: true,
            itemclick: toggleDataSeries
        },
        data: [{
                type: "column",
                name: "Volume",
                showInLegend: true,
                xValueFormatString: "DD MMMM YYYY",
                yValueFormatString: "##0",
                axisYType: "secondary",
                dataPoints: data_bar,
                color: 'orange'
            },
            {
                type: "spline",
                name: "Sentiment",
                showInLegend: true,
                yValueFormatString: "##0",
                dataPoints: data_line,
                lineThickness: 5,
                lineColor: 'black',
            },

        ]
    });
    chart.render();
}