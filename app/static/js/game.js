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
//            if (String(data[i][j]).replace('<br>','') != /^[1-9]$/){
//                alert("please in put number")
//                return
//            }
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
            result_json = JSON.parse(this.responseText)
            console.log(result_json)
            document.getElementById("result").innerHTML = result_json['game_result'];
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


//var btn=document.getElementById("submit_table")
//var div=document.getElementById('background')
//function show() {
//	div.style.display = "block";
//}
//
//window.addEventListener("resize", resizeCanvas, false);
//window.addEventListener("DOMContentLoaded", onLoad, false);
//window.requestAnimationFrame =
//window.requestAnimationFrame       ||
//window.webkitRequestAnimationFrame ||
//window.mozRequestAnimationFrame    ||
//window.oRequestAnimationFrame      ||
//window.msRequestAnimationFrame     ||
//function (callback) {
//  window.setTimeout(callback, 1000/60);
//};
//var canvas, ctx, w, h, particles = [], probability = 0.04,
//   xPoint, yPoint;
//function onLoad() {
//   canvas = document.getElementById("canvas");
//   ctx = canvas.getContext("2d");
//   resizeCanvas();
//   window.requestAnimationFrame(updateWorld);
//}
//
//function resizeCanvas() {
//   if (!!canvas) {
//       w = canvas.width = window.innerWidth;
//       h = canvas.height = window.innerHeight;
//   }
//}
//
//function updateWorld() {
//   update();
//   paint();
//   window.requestAnimationFrame(updateWorld);
//}
//
//function update() {
//   if (particles.length < 500 && Math.random() < probability) {
//       createFirework();
//   }
//   var alive = [];
//   for (var i=0; i<particles.length; i++) {
//       if (particles[i].move()) {
//           alive.push(particles[i]);
//       }
//   }
//   particles = alive;
//}
//
//function paint() {
//   ctx.globalCompositeOperation = 'source-over';
//   ctx.fillStyle = "rgba(0,0,0,0.2)";
//   ctx.fillRect(0, 0, w, h);
//   ctx.globalCompositeOperation = 'lighter';
//   for (var i=0; i<particles.length; i++) {
//       particles[i].draw(ctx);
//   }
//}
//
//function createFirework() {
//   xPoint = Math.random()*(w-200)+100;
//   yPoint = Math.random()*(h-200)+100;
//   var nFire = Math.random()*50+100;
//   var c = "rgb("+(~~(Math.random()*200+55))+","
//        +(~~(Math.random()*200+55))+","+(~~(Math.random()*200+55))+")";
//   for (var i=0; i<nFire; i++) {
//       var particle = new Particle();
//       particle.color = c;
//       var vy = Math.sqrt(25-particle.vx*particle.vx);
//       if (Math.abs(particle.vy) > vy) {
//           particle.vy = particle.vy>0 ? vy: -vy;
//       }
//       particles.push(particle);
//   }
//}
//
//function Particle() {
//   this.w = this.h = Math.random()*4+1;
//   this.x = xPoint-this.w/2;
//   this.y = yPoint-this.h/2;
//   this.vx = (Math.random()-0.5)*10;
//   this.vy = (Math.random()-0.5)*10;
//   this.alpha = Math.random()*.5+.5;
//   this.color;
//}
//
//Particle.prototype = {
//   gravity: 0.05,
//   move: function () {
//       this.x += this.vx;
//       this.vy += this.gravity;
//       this.y += this.vy;
//       this.alpha -= 0.01;
//       if (this.x <= -this.w || this.x >= screen.width ||
//           this.y >= screen.height ||
//           this.alpha <= 0) {
//               return false;
//       }
//       return true;
//   },
//   draw: function (c) {
//       c.save();
//       c.beginPath();
//       c.translate(this.x+this.w/2, this.y+this.h/2);
//       c.arc(0, 0, this.w, 0, Math.PI*2);
//       c.fillStyle = this.color;
//       c.globalAlpha = this.alpha;
//       c.closePath();
//       c.fill();
//       c.restore();
//   }
//}