document.addEventListener("DomContentLoaded", function(){
  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

  socket.on('connect', function(){
    document.querySelector('button').onclick =>(){
      const text = document.querySelector('text').value;
      socket.emit('sendmessage'),{'text':text,'channelid':{{channelid}}});
    });
  };

  socket.on('message relay', data => {
    document.querySelector('#chatlist').empty();
    data.chathistory.forEach(message => {
      const li=document.createElement('li');
      li.innerHTML=message;
      document.querySelector('#chatlist').append(li);
    })
  })
});
