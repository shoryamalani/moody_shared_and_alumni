// GLOBALS
const socket = io()
var client = {

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
}

// SOCKET HANDLERS
// socket.on('send_data_back', function(data) {
//     document.getElementById("receive").textContent = data["data"]
// })

socket.on("add_room", function(data) {
    room_div = document.getElementById("rooms_div")
    button = document.createElement("button")
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
    room_div = document.getElementById("rooms_div")
    for (var x = 0; x < data["rooms"].length; x++) {
        button = document.createElement("button")
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
})

function main() {
    //THIS IS WHERE ALL THE CODE WILL GO TO START FUNCTIONS
    get_id()
    get_rooms()
}

main()