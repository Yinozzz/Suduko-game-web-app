// the function is used to send a request with a url
function load_function(url, data, call_func){
    // IE7+, Firefox, Chrome, Opera, Safari
    xhttp=new XMLHttpRequest();
    xhttp.onreadystatechange=call_func;
    xhttp.open("POST",url,true);
    xhttp.setRequestHeader("content-type","application/json");
    xhttp.send(JSON.stringify(data));
}

//get input game information from table
function get_table_num(){
    table = document.getElementById("upload_table")
    data_string = ''
    data = []
    regexp_num = /^[1-9]$/;
    for(var i=0; i<table.rows.length ;i++){
        for(var j=0; j < table.rows[i].cells.length ;j++){
            if(!data[i]){
                data[i] = new Array()
            }
            data[i][j] = table.rows[i].cells[j].innerHTML
            if (!String(data[i][j]).replace('<br>','').match(regexp_num)){
                alert("please in put one number in each grid")
                return
            }
            if (String(data[i][j]).replace('<br>','') == ''){
                alert("please complete the upload table")
                return
            }

            data_string = data_string + String(data[i][j]).replace('<br>','') + ','
        }
    }



    var game_info = {"game_string":data_string.slice(0,-1)}
    var upload_url = "http://127.0.0.1:5000/upload"
    load_function(upload_url, game_info, function(){
        if (xhttp.status==200)
        {
            document.getElementById("result").innerHTML = this.responseText;
        }
    })
}

//get input game information from input string
function get_input_num(){
    // form = document.getElementById("getGameString")
    var regexp_string = /^([1-9],){80}[1-9]$/;
    var data_string=document.forms["getGameString"]["gameString"].value;
    if (data_string == null || data_string == ""){
        alert("please input game information before uploading.");
        return false;
    }
    if (!data_string.replace('<br>','').match(regexp_string)){
        alert("please input correctly formatted string.");
        return false;
    }


    var game_info = {"game_string":data_string}
    var upload_url = "http://127.0.0.1:5000/upload"
    load_function(upload_url, game_info, function(){
        if (xhttp.status==200)
        {
            document.getElementById("result").innerHTML = this.responseText;
        }else{
            document.getElementById("result").innerHTML = "fail";
        }
    })
}