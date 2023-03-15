// Load the Visualization API and the corechart package
google.charts.load('current', {'packages':['corechart']});

// Set a callback to run when the Google Visualization API is loaded
google.charts.setOnLoadCallback(drawChart);

// Define the function to draw the chart
function drawChart() {
  // Create a new DataTable
  var data = new google.visualization.DataTable();
  
  // Add columns to the DataTable
  data.addColumn('number', 'Year');
  data.addColumn('number', 'Sales');
  
  // Add rows to the DataTable
  var jsonData = [
    {"year": 2010, "sales": 100},
    {"year": 2011, "sales": 150},
    {"year": 2012, "sales": 200},
    {"year": 2013, "sales": 250},
    {"year": 2014, "sales": 300}
  ];
  for (var i = 0; i < jsonData.length; i++) {
    data.addRow([jsonData[i].year, jsonData[i].sales]);
  }

  // Set chart options
  var options = {
    title: 'Sales by Year',
    curveType: 'function',
    legend: { position: 'bottom' }
  };

  // Instantiate and draw the chart, passing in the options and the data
  var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
  chart.draw(data, options);
}