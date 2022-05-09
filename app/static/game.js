function get_table_num(){
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
    document.getElementById("number").value = data_string.slice(0,-1)
    document.getElementById("gameform").submit()
}

function start_game(){
    document.getElementById("game_table").style.display="table"
}
