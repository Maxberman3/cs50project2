document.addEventListener('DOMContentLoaded', () => {

    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // When connected, configure buttons
    socket.on('connect', () => {

        // Each button should emit a "submit vote" event
        document.querySelector('#messagesend').onclick = () => {
          const msgtxt=document.querySelector('#messagetext').value;
          socket.emit('messagesend',{"text":msgtxt});
        };
    });
    socket.on('message relay', data => {
        const li= document.createElement('li');
        li.innerHTML=data.text;
        document.querySelector('#chatlist').append(li);
    });
});
