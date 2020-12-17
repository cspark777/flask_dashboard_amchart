var Index = function () {

    return {        

        //main function
        init: function () {



            var polygonSeries = null;

            function get_main_page_data(){
                //Metronic.blockUI({boxed: true});
                var date_interval = 90;
                var country_filter = $('input[name="radio_country_filter"]:checked').val();
                $.ajax({
                    method: "POST",
                    url: "/get_mainpage",
                    data:{  "date_interval": date_interval, 
                            "country_filter": country_filter}
                })
                .done(function(msg) {      
                    var msg_obj = JSON.parse(msg);
                    var world_chart_data = msg_obj["world_chart_data"];
                    polygonSeries.data = world_chart_data
                    polygonSeries.invalidateRawData();

                    refresh_table(msg_obj["country_data"]);
                    //Metronic.unblockUI();
                })
                .fail(function(msg){
                    console.log(msg);   
                    //Metronic.unblockUI();       
                });
            }

            function create_line_charts(div_id, trend_data, is_positive){
                var len = trend_data["x"].length;
                var chart_data = []
                for (var i=0; i<len; i++){
                    var d = new Date(trend_data["x"][i]);
                    var t = {"date": d, "value": trend_data["y"][i]};
                    chart_data.push(t);
                }

                var chart = am4core.create(div_id, am4charts.XYChart);
                chart.logo.height = -15000;
                chart.paddingRight = 20;
                chart.data = chart_data;

                var dateAxis_line = chart.xAxes.push(new am4charts.DateAxis());
                dateAxis_line.renderer.inside = true;                    
                dateAxis_line.renderer.grid.template.disabled = true;
                dateAxis_line.renderer.labels.template.disabled = true;

                // Create value axis
                var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
                valueAxis.baseValue = 0;                                                
                valueAxis.renderer.grid.template.disabled = true;
                valueAxis.renderer.labels.template.disabled = true;

                // Create series
                var series = chart.series.push(new am4charts.LineSeries());
                series.dataFields.valueY = "value";
                series.dataFields.dateX = "date";
                if(is_positive)
                    series.stroke = am4core.color("#01e29a"); 
                else
                    series.stroke = am4core.color("#6a303f"); 

                series.strokeWidth = 5;
                series.tensionX = 0.77;                        
            }
            //===========================
            function refresh_table(detail_data){
                var table = $("#country_detail_table");
                var html = "";
                var len = detail_data.length;
                var tmp_str = "";
                for(var i=0;i<len;i++){
                    var detail = detail_data[i];
                    html = html + "<tr>";
                    html = html + '<td><a class="country-flag" href="/detail/' +detail["country"] + '"><img src="global/img/flags/' + detail["country"] + '.png">' + detail["country"] + '</a>' + "</td>";
                    if(detail["pulse_score"]>0){
                        html = html + '<td><div class="value-div m-auto positive">+' + detail["pulse_score"] + '</div></td>';
                    }
                    else{
                        if(detail["pulse_score"] == 0) detail["pulse_score"] = "-";
                        html = html + '<td><div class="value-div m-auto negative">' + detail["pulse_score"] + '</div></td>';
                    }

                    if(detail["30day_change"]>0){
                        html = html + '<td><div class="value-div m-auto positive-background positive">+' + detail["30day_change"] + '%</div></td>';
                    }
                    else{                            
                        if(detail["30day_change"] == 0)  tmp_str = "-";
                        else tmp_str = detail["30day_change"] + "%";
                        html = html + '<td><div class="value-div m-auto negative-background negative">' + tmp_str + '</div></td>';
                    }

                    //html = html + '<td><img class="trend-image" src="' + detail["trend_figure"] + '"></td>';
                    html = html + '<td><div class="line-chart-div" id="' + detail["country"] + '_chart"></td>';
                    
                    html = html + '<td><div class="value-div m-auto">' + detail["fx_price"] + '</div></td>';    
                                                
                    if(detail["daily_change"]>0){
                        html = html + '<td><div class="value-div m-auto positive-background positive">+' + detail["daily_change"] + '%</div></td>';    
                    }
                    else{
                        if(detail["daily_change"] == 0) tmp_str = "-";
                        else tmp_str = detail["daily_change"] + "%";
                        html = html + '<td><div class="value-div m-auto negative-background negative">' + tmp_str + '</div></td>';       
                    }                            
                    
                    html = html + "</tr>";
                }
                $("#country_detail_table tbody").html(html);

                for(var i=0;i<len;i++){
                    var detail = detail_data[i];
                    var div_id =  detail["country"] + "_chart";
                    if(detail["daily_change"]>0)
                        create_line_charts(div_id, detail["trend"], true);
                    else
                        create_line_charts(div_id, detail["trend"], false);
                }
            }

            $('input[name="radio_country_filter"]').on("click", function(e){
                
                get_main_page_data();
            });            

            $(document).on('click', "#country_detail_table tbody tr", function(e){
                var country = $(e.target.closest("tr")).find(".country-flag").text();
                window.location.href = "detail/" + country;
            });

            var d = new Date();
            var timeoffset = 0; //d.getTimezoneOffset() * 60000;

            am4core.useTheme(am4themes_animated);
            //am4core.useTheme(am4themes_dark);
            am4core.ready(function() {
                var data = [];

                var data_json = $("#init_chart_data").val();
                if(data_json != undefined)
                {
                    var data_obj = JSON.parse(data_json);
                    //===========================
                    var chart_heat = am4core.create("chartdiv_heat", am4maps.MapChart);
                    chart_heat.logo.height = -15000;
                    chart_heat.seriesContainer.draggable = false;
                    chart_heat.geodata = am4geodata_worldLow;
                    chart_heat.projection = new am4maps.projections.Miller();
                    var title = chart_heat.chartContainer.createChild(am4core.Label);
                    title.text = "09/28/2020";
                    title.fontSize = 20;
                    title.paddingTop = 30;
                    title.align = "center";

                    polygonSeries = chart_heat.series.push(new am4maps.MapPolygonSeries());
                    var polygonTemplate = polygonSeries.mapPolygons.template;
                    polygonTemplate.tooltipText = "{name}: {value.value}";
                    polygonSeries.useGeodata = true;
                    polygonSeries.heatRules.push({ property: "fill", target: polygonSeries.mapPolygons.template, min: am4core.color("#ff0000"), max: am4core.color("#00ff00") });
                    polygonSeries.exclude = ["AQ"];
                    chart_heat.maxZoomLevel = 1;


                    // add heat legend
                    var heatLegend = chart_heat.chartContainer.createChild(am4maps.HeatLegend);
                    heatLegend.valign = "bottom";
                    heatLegend.series = polygonSeries;
                    heatLegend.width = am4core.percent(100);
                    heatLegend.orientation = "vertical";
                    heatLegend.padding(30, 30, 30, 30);
                    heatLegend.valueAxis.renderer.labels.template.fontSize = 10;
                    heatLegend.valueAxis.renderer.minGridDistance = 40;

                    polygonSeries.mapPolygons.template.events.on("over", function (event) {
                        handleHover(event.target);
                    })

                    polygonSeries.mapPolygons.template.events.on("hit", function (event) {
                        handleHover(event.target);
                    })

                    function handleHover(mapPolygon) {
                        if (!isNaN(mapPolygon.dataItem.value)) {
                            heatLegend.valueAxis.showTooltipAt(mapPolygon.dataItem.value)
                        }
                        else {
                            heatLegend.valueAxis.hideTooltip();
                        }
                    }

                    polygonSeries.mapPolygons.template.events.on("out", function (event) {
                        heatLegend.valueAxis.hideTooltip();
                    })


                    // life expectancy data

                    polygonSeries.data = data_obj["world_chart_data"]

                    //============= for line charts on main table ===================

                    refresh_table(data_obj["country_data"]);

                    var interval;
                    function startInterval() {                        
                        interval = setInterval(get_main_page_data, 60000);
                    } 
                    startInterval();       
                }
            });
        },

    };

}();