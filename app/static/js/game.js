// count second
var second;
second=0;

var clock;

function startTimer()
{
    clock=setInterval(timer,1000);
}

function stopTimer() {
    clearInterval(clock);
    document.getElementById('sclock').innerHTML=second+'s';
}

function timer(){
    second++;
    document.getElementById('sclock').innerHTML=second+'s';
}





var start_time = 0
var finish_time = 0


// the function is used to send a request with a url
function load_function(url, data, call_func){
    // IE7+, Firefox, Chrome, Opera, Safari
    xhttp=new XMLHttpRequest();
    xhttp.onreadystatechange=call_func;
    xhttp.open("POST",url,false);
    xhttp.setRequestHeader("content-type","application/json");
    xhttp.send(JSON.stringify(data));
}

//Get user's  input number
function get_table_num(){
    var data_obj = new Date()
    finish_time = data_obj.getTime()
    table = document.getElementById("game_table")
    data_string = ''
    data = []
    regexp_num = /^[1-9]$/;
    for(var i=0; i<table.rows.length ;i++){
        for(var j=0; j < table.rows[i].cells.length ;j++){
            if(!data[i]){
                data[i] = new Array()
            }
            data[i][j] = table.rows[i].cells[j].innerHTML
            if (String(data[i][j]).replace('<br>','') == ''){
                alert("please complete the game")
                return
            }
            if (!String(data[i][j]).replace('<br>','').match(regexp_num)){
                alert("please in put one number in each grid")
                return
            }
            data_string = data_string + String(data[i][j]).replace('<br>','') + ','
        }
    }



    var game_info = {"start_time": start_time, "finish_time":finish_time, "game_string":data_string.slice(0,-1)}
    var game_url = "http://127.0.0.1:5000/game"
    load_function(game_url, game_info, function(){
        if (xhttp.status==200)
        {
            stopTimer()
            console.log(this.responseText)
            result_json = JSON.parse(this.responseText)
            console.log(result_json)
            document.getElementById("result").innerHTML = result_json['game_result'];

            if (result_json['game_result'] == 'congratulations!'){
                for(var i=0; i<table.rows.length ;i++){
                    for(var j=0; j < table.rows[i].cells.length ;j++){
                        table.rows[i].cells[j].setAttribute('contenteditable', "false")
                    }
                }
                document.getElementById("submit_table").style.display="none"
            }

            $("#rank_ul").empty();
            for (var i=0; i<result_json['rank_list'].length && i <= 14;i++){
                temp_li = document.createElement("li");
//                {{i}}. {{rank_line[i].player_name}}: best rank {{rank_line[i].best_mark}}
                temp_li.innerHTML = result_json['rank_list'][i]['rank'] + '. ' + result_json['rank_list'][i]['player_name'] + " Minimum completion time:" + result_json['rank_list'][i]['best_mark'] + 'S'
                document.getElementById("rank_ul").appendChild(temp_li)
            }
        }
    })
}

// game start
function start_game(){
    var data_obj = new Date()
    start_time = data_obj.getTime()
    document.getElementById("game_table").style.display="table"
    if (document.getElementById("start_button")){
        document.getElementById("start_button").style.display="none"
    }

    if (document.getElementById("start_button_no_user")){
        document.getElementById("start_button_no_user").style.display="none"
    }
}


