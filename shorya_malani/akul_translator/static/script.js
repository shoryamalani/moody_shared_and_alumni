const socket = io()

const data = { "want_to_be_a_kul": false }


function i_am_akul() {
    data["want_to_be_a_kul"] = true
    socket.emit("i_am_akul")
}

function akul_speaks() {
    socket.emit("akul_talking", { "words": document.getElementById("i_am_akul").value })
}

socket.on("akul_accepted", function() {

    if (data["want_to_be_a_kul"] == true) {
        alert("YOU HAVE BEEN ACCEPTED TO BE THE NEXT AKUL")
        document.getElementById("akul_div").hidden = false
    }
})


socket.on("akul_denied", function() {
    data["whoami"] = "akul"
    alert("Unfortunately due to access want for the position of the akul. We do not have space for you to be an akul. This may change with time but currently another holds the power")
})



socket.on("akul_says", function(data) {
    document.getElementById("akul_raw_text").textContent = data["akul_raw"]
    document.getElementById("akul_translated").textContent = data["final_string"]
})