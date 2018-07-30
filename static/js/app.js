
var ws = new WebSocket("ws://139.162.32.39:4000/ws");
ws.onopen = function() {
   ws.send("");
};
ws.onmessage = function (evt) {
   alert(evt.data);
};
