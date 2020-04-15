window.onload = function() {
    inactivityTime();
}
const socket = io.connect('http://battlecubing.shoryamalani.com');
socket.on('online', online => {
    document.getElementById('online').innerText = online;
});
var user_id = null
socket.on("get_id", id => {
    if (user_id == null) {
        user_id = id
    }
})
socket.on("scramble", scramble => {
    console.log(scramble)
    if (scramble[0] == room) {
        document.getElementById("scramble").innerHTML = scramble[1]
        start_solve()
    }
})
socket.on("new_solve", data => {
    console.log(data)
    if (data[0] == room) {
        var new_solve = document.createElement("tr")
        var name = document.createElement("td")
        name.innerHTML = data[1]
        var time = document.createElement("td")
        time.innerHTML = data[2]
        var average = document.createElement("td")
        average.innerHTML = data[3].toFixed(2)
        new_solve.append(name)
        new_solve.append(time)
        new_solve.append(average)
        document.getElementById("other_people").appendChild(new_solve)
    }
})
socket.on("start_solve", ids => {
    if (ids[0] == room) {
        console.log(ids)
        solving(ids[1])
    }
})
window.addEventListener("beforeunload", function(e) {
    socket.emit("disconnect", user_id)
    timer_on = "off"

}, false);
window.addEventListener('keyup', function(event) {
    const key = event.key; // "a", "1", "Shift", etc.
    console.log(key)
    if (key == "r" && stage == 1 && ready == false) {
        socket.emit("ready", [room, user_id])
        timer_on = "off"
        document.getElementById('solve_timer').innerHTML = "Get ready for inspection"
        document.getElementById('solve_timer').style = "color:black"
        ready = true

    }
});
window.addEventListener('keyup', function(event) {
    solve_time = new Date().getTime() - time_solve
    solve_time = solve_time / 1000
    const key = event.key; // "a", "1", "Shift", etc.
    console.log(key)
    if (key == " " && stage == 3) {
        document.getElementById('solve_timer').style = "color:black"
        stage = 4

    } else if (key == " " && stage == 4 && solve_time > 2) {
        document.getElementById('solve_timer').style = "color:pink"
        stage = 5

    }
});
var room = null

function join_room(number) {
    console.log(number)
    socket.emit("join_room", [user_id, number, document.getElementById("name").value])
    room = number
    document.getElementById("startup").hidden = true
    document.getElementById("solving").hidden = false
}
var inactivityTime = function() {
    var time;
    window.onload = resetTimer;
    // DOM Events
    document.onmousemove = resetTimer;
    document.onkeypress = resetTimer;

    function logout() {
        socket.emit("disconnect", user_id)
        alert("You are now logged out.")
            //location.href = 'logout.html'
    }

    function resetTimer() {
        clearTimeout(time);
        time = setTimeout(logout, 120000)
            // 1000 milliseconds = 1 second
    }
};
var stage = 0
var solve_num = 0
var timer_on = "on"
var ready = null
var solved;
async function start_solve() {
    solved = false
    document.getElementById('solve_timer').style = "color:black"
    ready = false
    var sec = 45.00;
    stage = 1
    timer_on = "on"
    while (timer_on == "on") {
        document.getElementById('solve_timer').innerHTML = sec.toFixed(2);
        await sleep(500)
        sec -= .5;
        if (sec == 0) {
            timer_on = "off"
        }

    }
    stage = 2
    if (ready == false) {
        socket.emit("ready", [room, user_id])
    }
    document.getElementById('solve_timer').innerHTML = "Get ready for inspection"
    ready = true
}
var time_solve = null
var solve_special = 0
async function solving(start_time) {

    if (stage == 2) {
        var time_now = new Date().getTime()
        console.log(start_time)
        console.log(time_now)
        var sec = (start_time - time_now)
        sec = sec / 1000
        console.log(sec)
        timer_on = "on"
        document.getElementById('solve_timer').style = "color:red"
        while (timer_on == "on") {
            document.getElementById('solve_timer').innerHTML = sec.toFixed(2);
            await sleep(200)
            sec -= .2;
            if (sec <= 0) {
                timer_on = "off"
                stage = 3
            }
        }
        sec = 0

        while (stage == 3) {
            document.getElementById('solve_timer').style = "color:blue"
            document.getElementById('solve_timer').innerHTML = sec.toFixed(2);
            await sleep(200)
            sec += .2;
            if (sec == 15) {
                timer_plus = "on"
                sec = 2
                while (timer_plus == "on") {
                    sec += .2;
                    await sleep(200)
                    document.getElementById('solve_timer').innerHTML = "+2";
                    solve_special = 0
                    if (sec == 17) {
                        timer_plus = "off"
                        solve_special = 4
                    }
                }
            }

        }
        sec = 0
        time_solve = new Date().getTime()
        while (stage == 4) {
            document.getElementById('solve_timer').innerHTML = sec.toFixed(2);
            await sleep(100)
            sec += .1;
        }

        solve_time = new Date().getTime() - time_solve
        solve_time = solve_time / 1000
        if (solved == false) {
            solved = true
            document.getElementById('solve_timer').innerHTML = solve_time;
            socket.emit("solved", [room, user_id, solve_time])
            document.getElementById("other_people").innerHTML = "<tr><th>name</th><th>Time</th><th>average</th></tr>"
            solve_num++
            var new_solve = document.createElement("tr")
            var name = document.createElement("td")
            name.innerHTML = solve_num
            var time = document.createElement("td")
            time.innerHTML = solve_time
            new_solve.append(name)
            new_solve.append(time)
            document.getElementById("old_solves").append(new_solve)
        }
    }


}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
// socket.on('win',win=>{
//   alert("You won")
//   socket.emit("reset","full")
//   cases_at_once = 1
//   cases_leftover = 0
//   upgrade_number = 0
//   cash_to_add = 1
//   cash = 0
//   time = 5000
//   auto_cash = 0
//   auto_healers = 0  
// });
// socket.on('lose',win=>{
//   alert("You lost")
//   socket.emit("reset","full")
//   cases_at_once = 1
//   cases_leftover = 0
//   upgrade_number = 0
//   cash_to_add = 1
//   cash = 0
//   time = 5000
//   auto_cash = 0
//   auto_healers = 0  
// });
// var btn = document.getElementById('btn');
// var cases = document.getElementById('clickCount');
// //var final_cases = cases - 1;
// var clickCounter = document.getElementById('clickCount');



// // ("#btn").click(function() {

// // });


// // btn.addEventListener('click', function() {
// // 	socket.emit('clicks', 'duh');
// // });
// var upgrades = {cash_for_upgrades : [25,150,1000,5000,10000],25:["Get a Job","Hire help"],150:["Raining Cash","More medical workers"],1000:["Auto Healers","Too much cash"],5000:["Even more medical workers","Auto Cash","Enough cash to buy a car"],10000:["Public Awareness Campaign"]}
// var cases_at_once = 1
// var cases_leftover = 0
// var upgrade_number = 0
// function clicked(){
//   cases_leftover = cases_leftover+ cases_at_once - Math.floor(cases_leftover)
//   console.log(cases_leftover)
//   socket.emit('clicks', Math.floor(cases_at_once));
//   if (cases_leftover=== parseInt(cases_leftover,10) && cases_leftover!=0){
//     socket.emit('clicks', cases_leftover);
//     console.log(cases_leftover)
//     cases_leftover = 0
//   }
// }
// // function reset_count(){
// //   socket.emit('reset',"pls")
// // }
// var cash_to_add = 1
// var cash = 0
// function add_money(){
//   cash +=cash_to_add
//   document.getElementById("money").innerText = cash
//   if(cash>= upgrades["cash_for_upgrades"][0]){
//     for(var u=0;u<upgrades[upgrades["cash_for_upgrades"][0]].length;u++){
//       var button = document.createElement("BUTTON")
//       button.className = "button upgrade"
//       button.id="upgrade"+upgrade_number
//       button.setAttribute("onclick","buy_upgrade("+upgrades["cash_for_upgrades"][0]+",'"+upgrades[upgrades["cash_for_upgrades"][0]][u]+"','upgrade"+upgrade_number+"')")
//       var price_span = document.createElement("SPAN")
//       price_span.innerText = upgrades["cash_for_upgrades"][0]+":"
//       price_span.className = "price"
//       var upgrade_span = document.createElement("SPAN")
//       upgrade_span.innerText = upgrades[upgrades["cash_for_upgrades"][0]][u]
//       price_span.className = "upgrade"
//       button.appendChild(price_span)
//       button.appendChild(upgrade_span)
//       var upgrade_div =document.getElementById("upgrades_div")
//       upgrade_div.append(button)
//       upgrade_number++

//     }
//     upgrades["cash_for_upgrades"].shift()
//   }
// }

// function buy_upgrade(price,upgrade,id){
//   if(cash>price){  
//     cash=cash-price
//     document.getElementById("money").innerText = cash
//     document.getElementById(id).hidden=true
//     if (upgrade =="Get a Job"){
//       cash_to_add++
//     }else if(upgrade =="Hire help"){
//       cases_at_once+=.2
//     }else if(upgrade =="More medical workers"){
//       cases_at_once+=2
//     } else if(upgrade =="Raining Cash"){
//       cash_to_add+=5
//     }else if(upgrade =="Too much cash"){
//       cash_to_add+=25
//     }else if(upgrade =="Auto Healers"){
//       auto_healers +=10
//     }else if(upgrade =="Auto Cash"){
//       auto_cash +=80
//     }else if(upgrade =="Even more medical workers"){
//       cases_at_once+=10
//     }else if(upgrade =="Enough cash to buy a car"){
//       cash_at_once+=200
//     }else if(upgrade =="Public Awareness Campaign"){
//       socket.emit('case_time')
//     }     
// }}
// socket.on("cases",function(cases){
//   document.getElementById("clickCount").textContent = Math.round(cases)
// })
// // socket.on('clicks', function(clicks) {
// // 	clickCounter.innerHTML = '${clicks};'
// // });
// var time = 5000
// var auto_cash = 0
// var auto_healers = 0
// setInterval(function(){
//   socket.emit('clicks',auto_healers);
// }, time)