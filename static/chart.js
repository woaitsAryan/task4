// read local JSON file in javascript
let jsDataString=(document.querySelector(".jsData").innerHTML);
jsDataString="["+ jsDataString.substring(1, jsDataString.length -1)  +"]"

jsData=JSON.parse(jsDataString);

console.log(jsData)
function sort_datearr(datearr){
  return datearr.sort((a,b)=>new Date(a).getTime()-new Date(b).getTime());
}

fetch("data1.json")
  .then(function (response) {
    return response.json();
  })
  .then(function (jsData) {
    // Load the Visualization API and the corechart package
    google.charts.load('current', {'packages':['corechart']});

    // Set a callback to run when the Google Visualization API is loaded
    google.charts.setOnLoadCallback(drawChart);

    // Define the function to draw the chart
    function drawChart() {
      let date_array=[];
      // Create a new DataTable
      var data = new google.visualization.DataTable();
      
      // Add columns to the DataTable
      data.addColumn('date', 'Date');
      data.addColumn('number', 'Cases');
      
      // Add rows to the DataTable
      for (var i = 0; i < jsData.length; i++) {
        date_array[i]=jsData[i].data;
      }
      let sortedDateArray=sort_datearr(date_array);
      console.log(sortedDateArray);

      for (var i = 0; i < jsData.length; i++) {
        var date = new Date(sortedDateArray[i]);
        var cases = jsData[i].cases_new;
        data.addRow([date, cases]);
      }

      // Set chart options
      var options = {
        title: 'Daily New Cases',
        curveType: 'LINEAR',
        color:['#e2431e'],
        legend: { position: 'bottom' },
        axes: {
          y: {
            0: {side: 'bottom'}
          }
        }
      };

      // Instantiate and draw the chart, passing in the options and the data
      var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
      chart.draw(data, options);
    }
  });
