// GLOBALS
const socket = io()
var client = {
    name: ""
}

//FUNCTIONS FOR FOR WORKING
function get_id() {
    // var get_id = window.setInterval(function() {
    //     if (!client["id"]) {
    socket.emit("get_id")
        //     }
        // }, 3000)
}

function get_rooms() {
    socket.emit("get_rooms")
}

function send_data() {
    const input = document.getElementById("testing_inputs").value
    socket.emit('send_data', { "data_sent": input })
}

function send_name() {
    const input = document.getElementById("name").value
    socket.emit('send_name', { "data_sent": input })
    client["name"] = input
}

function create_game() {
    game_name = prompt("What is the name of your game", "Blobs_game")
    socket.emit("create_room", { "data": game_name, "id": client["id"] })
    client["game"] = game_name
}

function choose_game(game) {
    document.getElementById("pick_game").hidden = true
    document.getElementById("game_div").hidden = false
    socket.emit("choose_game", { "game": game, "game_name": client["game"] })
}

function join_room(name) {
    socket.emit("join_room", { "name": name, "id": client["id"] })
    client["game"] = name
}


// SOCKET HANDLERS
// socket.on('send_data_back', function(data) {
//     document.getElementById("receive").textContent = data["data"]
// })

socket.on('new_player', function(data) {
    if (!(data["name"] == client["name"])) {
        if (!(data["name"] == client["id"])) {
            players = document.getElementById("players")
            new_player = document.createElement("p")
            new_player.textContent = data["name"]
            players.append(new_player)
            alert(data["name"] + " has joined.")
        }
    }
})

socket.on("pick_game", function(data) {
    var file_name = data["game"] + ".html"
    $("#inner_game_div").load(file_name)
        // document.getElementById(data["game"]).hidden = false
    document.getElementById("game_name").textContent = data["game"]
})

socket.on("add_room", function(data) {
    var room_div = document.getElementById("rooms_div")
    var button = document.createElement("button")
    button.textContent = data["name"]
    button.setAttribute("class", "pure-button")
    button.setAttribute("onclick", "join_room('" + data["name"] + "')")
    room_div.appendChild(document.createElement("BR"))
    room_div.appendChild(button)
})
socket.on('set_id', function(data) {
    client["id"] = data["id"]
})
socket.on('room_taken', function() {
    alert("That room name is taken")
})
socket.on('get_rooms', function(data) {
    var room_div = document.getElementById("rooms_div")
    for (var x = 0; x < data["rooms"].length; x++) {
        var button = document.createElement("button")
        button.textContent = data["rooms"][x]
        button.setAttribute("class", "pure-button")
        button.setAttribute("onclick", "join_room('" + data["rooms"][x] + "')")
        room_div.appendChild(document.createElement("BR"))
        room_div.appendChild(button)
    }
})
socket.on('start_game', function(data) {
    document.getElementById("setup_rooms").hidden = true
    document.getElementById("pick_game").hidden = false
    var players = document.getElementById("players")
    var new_player = document.createElement("p")
    var name = client["id"]
    if (client["name"] != "") {
        name = client["name"]
    }
    new_player.textContent = name
    players.append(new_player)
})

socket.on("join_game", function(data) {
    document.getElementById("setup_rooms").hidden = true
    document.getElementById("game_div").hidden = false
    var players = document.getElementById("players")
    for (var x = 0; x < data["players"].length; x += 1) {
        var new_player = document.createElement("p")
        new_player.textContent = data["players"][x]
        players.append(new_player)
    }
    document.getElementById("game_name").textContent = data["game"]
    if (data["game"] != "") {
        document.getElementById(data["game"]).hidden = false
    }
})


// THIS IS WHERE WE HAVE THE JAMES BOND FUNCTIONS

function james_interpreter(data) {
    if (data["action"] == "start_game") {
        console.log("")
    }
}

function main() {
    //THIS IS WHERE ALL THE CODE WILL GO TO START FUNCTIONS
    get_id()
    get_rooms()
}

main()