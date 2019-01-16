// FOR CHANGING COLOR OF THE TABLE ROW WHILE HOVER 
$(document).ready(function(){
    $(' #all_data_table > tbody > tr').hover(function(){
        $(this).addClass('hovered_row');
        }, function(){
        $(this).removeClass('hovered_row');
        });    
    });

// ###########################################################################################################################
// FOR SHOWING ACTUAL TIME (EACH TIME SUBSTITUTE DIV CLOCK)
function time()
{
    var actual_date = new Date();

    var actual_day = actual_date.getDate();
    if (actual_day < 10) actual_day = "0" + actual_day; 

    var actual_month = actual_date.getMonth()+1;
    if (actual_month < 10) actual_month = "0" + actual_month;

    var actual_year = actual_date.getFullYear();

    var actual_second = actual_date.getSeconds();
    if (actual_second < 10) actual_second = "0" + actual_second;

    var actual_minute = actual_date.getMinutes();
    if (actual_minute < 10) actual_minute = "0" + actual_minute;

    var actual_hour = actual_date.getHours();
    if (actual_hour < 10) actual_hour = "0" + actual_hour;

    $('#clock').html(actual_hour +":"+ actual_minute +":"+ actual_second +" "+ actual_day +"/"+ actual_month +"/"+ actual_year);

    setTimeout("time()", 1000)
}