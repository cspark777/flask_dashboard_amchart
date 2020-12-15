var Detail = function () {

    return {

        //main function
        init: function () {
            var d = new Date();
            var timeoffset = 0; //d.getTimezoneOffset() * 60000;
            
            //am4core.useTheme(am4themes_dark);
            am4core.ready(function() {
                am4core.useTheme(am4themes_animated);

                var data = [];

                var data_json = $("#init_chart_data").val();
                if(data_json != undefined)
                {
                    var data_obj = JSON.parse(data_json);
                    //===========================
                    var len = data_obj["trend"]["x"].length;
                    var trend_data = []
                    for (var i=0; i<len; i++){
                        var d = new Date(data_obj["trend"]["x"][i]);
                        var t = {"date": d, "value": data_obj["trend"]["y"][i]};
                        trend_data.push(t);
                    }

                    var chart = am4core.create("country_detail_chart", am4charts.XYChart);
                    chart.logo.height = -15000;
                    chart.paddingRight = 20;
                    chart.data = trend_data;

                    var dateAxis_line = chart.xAxes.push(new am4charts.DateAxis());
                    dateAxis_line.renderer.inside = true;                    
                    dateAxis_line.renderer.grid.template.disabled = true;

                    // Create value axis
                    var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
                    valueAxis.baseValue = 0;
                    valueAxis.renderer.grid.template.stroke = "#888888";

                    // Create series
                    var series = chart.series.push(new am4charts.LineSeries());
                    series.dataFields.valueY = "value";
                    series.dataFields.dateX = "date";
                    series.stroke = am4core.color("#01e29a"); 
                    series.strokeWidth = 5;
                    series.tensionX = 0.77;

                    // bullet is added because we add tooltip to a bullet for it to change color
                    var bullet = series.bullets.push(new am4charts.Bullet());
                    bullet.tooltipText = "{valueY}";

                    bullet.adapter.add("fill", function(fill, target){
                        if(target.dataItem.valueY < 0){
                            return am4core.color("#FF0000");
                        }
                        return fill;
                    })

                    chart.cursor = new am4charts.XYCursor();


                    //===========================
                    
                    function refresh_summary_table(summary_data){
                                                
                        $("#country_flag_img").attr("src", "/global/img/flags/" + summary_data["country"] + ".png");

                        $("#country_name").html(summary_data["country_name"]);

                        var html = "<tr>";
                        html = html + "<td>" + summary_data["survey"] + "%</td>"; 

                        if(summary_data["growth"] > 0){
                            html = html + '<td class="positive">+' + summary_data["growth"] + '%</td>';
                        }
                        else{
                            html = html + '<td class="negative">' + summary_data["growth"] + '%</td>';
                        }

                        html = html + "<td>" + summary_data["emplovment"] + "%</td>"; 

                        if(summary_data["inflation"] > 0){
                            html = html + '<td class="positive">+' + summary_data["inflation"] + '%</td>';
                        }
                        else{
                            html = html + '<td class="negative">' + summary_data["inflation"] + '%</td>';
                        }


                        html = html + "<td>" + summary_data["housing"] + "%</td>";
                        html = html + '</tr>';

                        //---
                        html = html + '<tr>';                        
                        html = html + '<td colspan="2"><div class="border-btn">';
                        if(summary_data["current_reading"] > 0){
                            html = html + '<p class="positive">+' + summary_data["current_reading"] +'</p>';
                        }
                        else{
                            html = html + '<p class="negative">' + summary_data["current_reading"] +'</p>';
                        }
                        html = html + '<p>Current Reading</p></div></td>';
                        
                        html = html + '<td colspan="2"><div class="border-btn">';
                        if(summary_data["prev_reading"] > 0){
                            html = html + '<p class="positive">+' + summary_data["prev_reading"] +'</p>';
                        }
                        else{
                            html = html + '<p class="negative">' + summary_data["prev_reading"] +'</p>';
                        }
                        html = html + '<p>Prev Reading</p></div></td>';

                        if(summary_data["status"] == 1){
                            $("#arror_img").attr("src", "/global/img/up.png");
                        }
                        else{
                            $("#arror_img").attr("src", "/global/img/down.png");
                        }

                        $("#country_summary_info_table tbody").html(html);

                        //----- country_data_detail_table 

                        var len = summary_data["data_detail"].length;
                        html = "";
                        for(var i=0;i<len;i++){
                            var detail = summary_data["data_detail"][i];
                            html = html + "<tr>";
                            html = html + '<td>' + detail["pulse_detail"] + '</td>';
                            html = html + '<td>' + detail["sector"] + '</td>';

                            if(detail["current_reading"] > 0){
                                html = html + '<td><div class="positive">' + detail["current_reading"] + '%</div></td>';                                
                            }
                            else{
                                html = html + '<td><div class="negative">' + detail["current_reading"] + '%</div></td>';   
                            }

                            html = html + '<td>' + detail["prev_reading"] + '%</td>';

                            if(detail["status"] == 1){
                                html = html + '<td><div class="value-div positive-background positive">Improving</div></td>';
                            }
                            else if(detail["status"] == 0){
                                html = html + '<td><div class="value-div steady-background">Steady</div></td>';
                            }
                            else{
                                html = html + '<td><div class="value-div negative-background negative">Negative</div></td>';
                            }

                            html = html + '</tr>'

                        }
                        $("#country_data_detail_table tbody").html(html);
                    }

                    refresh_summary_table(data_obj);
                    
                    // add data
                    var interval;
                    function startInterval() {
                        interval = setInterval(function() {                
                            $.ajax({
                                method: "POST",
                                url: "/get_mainpage",
                                data:{"date_interval": 90}
                            })
                            .done(function(msg) {      
                                var msg_obj = JSON.parse(msg);
                                var world_chart_data = msg_obj["world_chart_data"];
                                polygonSeries.data = world_chart_data
                                polygonSeries.invalidateRawData();
                            })
                            .fail(function(msg){
                                console.log(msg);          
                            });

                        }, 6000);
                    } 

                    //startInterval();       
                }
            });
        },

    };

}();