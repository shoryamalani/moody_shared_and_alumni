//GLOBALS
const socket = io()

function send_data() {
    const input = document.getElementById("testing_inputs").value
    socket.emit('send_data', { "data_sent": input })
}
socket.on('send_data_back', function(data) {
    document.getElementById("receive").textContent = data["data"]
})

function main() {
    //THIS IS WHERE ALL THE CODE WILL GO TO START FUNCTIONS

}
main()