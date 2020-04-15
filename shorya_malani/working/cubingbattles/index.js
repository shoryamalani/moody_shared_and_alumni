 //DEPENDENCIES
 const express = require('express');
 const fs = require("fs");
 const socket = require('socket.io');
 const parse = require('scramble-parser');
 const preview = require('cube-preview');
 const cubeScrambler = require("cube-scrambler")();


 // let clicks = fs.readFileSync('public/count.txt').toString();
 // let cases = fs.readFileSync('public/cases.txt')
 // function roundNumber(num, scale) {
 //   if(!("" + num).includes("e")) {
 //     return +(Math.round(num + "e+" + scale)  + "e-" + scale);
 //   } else {
 //     var arr = ("" + num).split("e");
 //     var sig = ""
 //     if(+arr[1] + scale > 0) {
 //       sig = "+";
 //     }
 //     return +(Math.round(+arr[0] + "e" + sig + (+arr[1] + scale)) + "e-" + scale);
 //   }
 // }
 function sleep(ms) {
     return new Promise(resolve => setTimeout(resolve, ms));
 }

 // //SERVER
 const app = express();
 const server = app.listen('http://localhost:3000', () => {});

 app.use(express.static('public'));

 //SOCKET.IO
 const io = socket(server);

 const GameData = {
     online: 0,
     rooms: { 1: { "users": [], "ready": 0, "solved": 0 }, 2: { "users": [], "ready": 0, "solved": 0 }, 3: { "users": [], "ready": 0, "solved": 0 }, 4: { "users": [], "ready": 0, "solved": 0 } },
     users: {}
 }
 io.on('connection', socket => {

     GameData.online++
         var player_id = Math.round(Math.random() * 10 ** 16)
     GameData.users[player_id] = { "room": null, "solves": [] }
     io.sockets.emit('online', GameData.online);
     console.log(player_id)
     io.sockets.emit('get_id', player_id);
     // 	io.sockets.emit('clicks', clicks);

     socket.on('disconnect', socket => {
         GameData.online--
             if (GameData.users[player_id]["room"] != null) {
                 for (var i = GameData.rooms[GameData.users[player_id]["room"]]["users"].length - 1; i >= 0; i--) {
                     if (GameData.rooms[GameData.users[player_id]["room"]]["users"][i] === player_id) {
                         GameData.rooms[GameData.users[player_id]["room"]]["users"].splice(i, 1);
                     }
                 }
             }
         delete GameData.users[player_id]
         console.log(player_id)
         io.sockets.emit('online', GameData.online);
     })
     socket.on("join_room", info => {
         if (info[2] == "put your name here") {
             info[2] = info[0]
         }
         GameData.users[info[0]]['name'] = info[2]
         GameData.users[info[0]]['room'] = info[1]
         GameData.rooms[info[1]]["users"].push(info[0])
         console.log(GameData.rooms[info[1]]["users"].length)
         if (GameData.rooms[info[1]]["users"].length == 1) {
             start_room(info[1])
         }
     })
     socket.on("ready", ids => {
         GameData["rooms"][ids[0]].ready++
     })
     socket.on("solved", ids => {
         console.log("test")
         GameData["rooms"][ids[0]].solved++
             GameData["users"][ids[1]]["solves"].push(ids[2])
         if (GameData["users"][ids[1]]["solves"].length) {
             var sum = GameData["users"][ids[1]]["solves"].reduce(function(a, b) { return a + b; });
             var avg = sum / GameData["users"][ids[1]]["solves"].length;
         }
         console.log(ids[0], GameData["users"][ids[1]].name, ids[2], avg)
         io.sockets.emit("new_solve", [ids[0], GameData["users"][ids[1]].name, ids[2], avg])
     })
 });
 var room_times = [20, 30, 40, 120]
 async function start_room(room) {
     while (GameData.rooms[room]["users"].length != 0) {
         GameData["rooms"][room].ready = 0
         console.log(GameData.rooms[room]["users"].length)
         var scramble = cubeScrambler.scramble();
         io.sockets.emit('scramble', [room, scramble])
         for (let i = 0; i < 16; i++) {
             if (GameData["rooms"][room].ready >= GameData["rooms"][room]["users"].length) {
                 i = 16
             }
             await sleep(3000);
             console.log(i);
         }
         var date = new Date().getTime()
         date += 10000
         console.log(date)
         io.sockets.emit('start_solve', [room, date])
         var ready_time = 0

         while (GameData["rooms"][room].ready > GameData["rooms"][room].solved && ready == false) {
             await sleep(1000);
             ready_time += 1
             if (ready_time >= room_times[room]) {
                 ready = true
             }
         }
         GameData["rooms"][room].solved = 0
         GameData["rooms"][room].ready = 0
         ready = false
     }

     // scramble = cubeScrambler.scramble();e
     // io.sockets.emit('scramble',scramble)
     // console.log(scramble)
 }
 //   socket.on("clicks", (clickCount) => {
 //     clicks = Number(clicks)
 //     clicks += Number(clickCount)
 //     io.sockets.emit("clicks", clicks)
 //   });
 //   socket.on("case_time",()=>{
 //     increase = increase-0.01
 //   })
 //   socket.on('reset',(count)=>{
 //     cases = 10000
 //     clicks=0
 //     fs.writeFile('public/cases.txt', cases, function (err) {console.log(err)});
 //     fs.writeFile('public/count.txt', clicks, function (err) {
 //   if (err) throw err;});
 //     time_for_adding_cases = 3500
 //     increase = 1.01; 

 //   })
 //   /*socket.on("lose", () => {
 //     clicks = 0
 //   })

 //   socket.on("win", () => {
 //     clicks = 0
 //   })*/

 // var time_for_adding_cases = 3500
 // setInterval(function(){
 //   // let increase = 1.01;
 //   // fs.writeFile('public/count.txt', clicks, function (err) {
 //   // if (err) throw err;
 //   // cases = fs.readFileSync('public/cases.txt'),2
 //   // if (cases > 8000000) {
 //   //   io.sockets.emit("lose")
 //   //   }else if (cases == 0) {
 //   //     io.sockets.emit("win")
 //   // }
 //   // fs.writeFile('public/cases.txt', cases*increase, function (err) {
 //   // if (err) throw err;

 //   // scramble = cubeScrambler.scramble();
 //   // io.sockets.emit('scramble',scramble)
 //   // console.log(scramble)


 // }, 40000)