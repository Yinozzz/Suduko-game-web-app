var start_time = 0
var finish_time = 0


// the function is used to send a request with a url
function load_function(url, data, call_func){
    // IE7+, Firefox, Chrome, Opera, Safari
    xhttp=new XMLHttpRequest();
    xhttp.onreadystatechange=call_func;
    xhttp.open("POST",url,true);
    xhttp.setRequestHeader("content-type","application/json");
    xhttp.send(JSON.stringify(data));
}


function get_table_num(){
    var data_obj = new Date()
    finish_time = data_obj.getTime()
    table = document.getElementById("game_table")
    data_string = ''
    data = []
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
            data_string = data_string + String(data[i][j]).replace('<br>','') + ','
        }
    }

//    document.getElementById("number").value = data_string.slice(0,-1)
//    document.getElementById("gameform").submit()

    var game_info = {"start_time": start_time, "finish_time":finish_time, "game_string":data_string.slice(0,-1)}
    var game_url = "http://127.0.0.1:5000/game"
    load_function(game_url, game_info, function(){
        if (xhttp.status==200)
        {
            document.getElementById("result").innerHTML = this.responseText;
        }
    })
}

function start_game(){
    var data_obj = new Date()
    start_time = data_obj.getTime()
    document.getElementById("game_table").style.display="table"
}
