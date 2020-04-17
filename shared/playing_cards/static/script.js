function set_up_socket() {
    const socket = io()
    return socket
}


function main() {
    socket = set_up_socket()
}
main()