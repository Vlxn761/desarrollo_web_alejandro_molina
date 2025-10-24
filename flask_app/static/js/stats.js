Highcharts.chart("grafico-lineas", {
  chart: {
    type: "line",
  },
  title: {
    text: "Avisos de adopción agregados por día",
  },
  xAxis: {
    type: "datetime",
    dateTimeLabelFormats: {
      month: "%b %e, %Y",
    },
    title: {
      text: "Fecha",
    },
  },
  yAxis: {
    title: {
      text: "Numero de Avisos",
    },
  },
  legend: {
    align: "left",
    verticalAlign: "top",
    borderWidth: 0,
  },

  tooltip: {
    shared: true,
    crosshairs: true,
  },

  series: [
    {
      name: "Avisos",
      data: [],
      lineWidth: 1,
      marker: {
        enabled: true,
        radius: 4,
      },
      color: "#0077b6",
    },
  ],
});

Highcharts.chart('grafico-torta', {
    chart: {
        type: 'pie'
    },
    title: {
        text: 'Proporción de Avisos por tipo de Mascota'
    },
    series: [{
        name: 'Cantidad',
        data: [],
        dataLabels: {
            enabled: true,
            format: '{point.name}<br>{point.y} avisos'
        }
    }],
    tooltip: {
        pointFormat: '<b>{point.y}</b> avisos'
    }
});

Highcharts.chart('grafico-barra', {
    chart: {
        type: 'column'
    },
    title: {
        text: 'Cantidad de Avisos por Mes y Tipo'
    },
    xAxis: {
        categories: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    },
    yAxis: {
        min: 0,
        title: {
            text: 'Cantidad de Avisos'
        }
    },
    series: [{
        name: 'Perros',
        data: []
    }, {
        name: 'Gatos',
        data: []
    }],
    tooltip: {
        shared: true,
        valueSuffix: ' avisos'
    }
});

fetch("http://127.0.0.1:5000/estadisticas-dia")
    .then((response) => response.json())
    .then((data) => {
    let parsedData = data.map((item) => {
      const [year, month, day] = item.fecha
        .split("-")
        .map((part) => parseInt(part, 10));
      return [
        Date.UTC(year, month - 1, day), 
        item.cantidad,
      ];
    });

    const chart = Highcharts.charts.find(
      (chart) => chart && chart.renderTo.id === "grafico-lineas"
    );

    chart.update({
      series: [
        {
          data: parsedData,
        },
      ],
    });
  })
  .catch((error) => console.error("Error:", error));

fetch("http://127.0.0.1:5000/estadisticas-tipo")
    .then((response) => response.json())
    .then((data) => {
    data = data.map((item) => {
      if (item.tipo == "perro") tipo = "Perros";
      else tipo = "Gatos";
      return [
        tipo, 
        item.cantidad,
      ];
    });
    const chart = Highcharts.charts.find(
      (chart) => chart && chart.renderTo.id === "grafico-torta"
    );

    chart.update({
      series: [
        {
          data: data,
        },
      ],
    });
  })
  .catch((error) => console.error("Error:", error));

fetch("http://127.0.0.1:5000/estadisticas-mes")
    .then((response) => response.json())
    .then((data) => {
    const chart = Highcharts.charts.find(
      (chart) => chart && chart.renderTo.id === "grafico-barra"
    );
    console.log(data)
    chart.update({
      series: [
        {
          data: data.perros
        }, {
          data: data.gatos
        }
      ],
    });
  })
  .catch((error) => console.error("Error:", error));