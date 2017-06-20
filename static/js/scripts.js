var getCookie = function(name) {
    name = name + "=";

    var ca = document.cookie.split(';');

    for(var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) === ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) === 0) {
            return c.substring(name.length, c.length);
        }
    }
    return;
}

var showForm = function() {
    document.getElementById('text').style.display = 'none';
    document.getElementById('form').style.display = 'block';
}

var showText = function(unsafe, safe) {
    unsafe = unsafe || '';
    safe = safe || '';

    document.getElementById('form').style.display = 'none';
    document.getElementById('text').style.display = 'block';
    document.getElementById('text-unsafe').innerHTML = unsafe;
    document.getElementById('text-safe').innerHTML = safe;
}

zvent.subscribe(/^$/, function() {
    showForm();
});


zvent.subscribe(/^send-message$/, function(request) {
    showText('Enviando...');
    ajax({
        url: '/api-rest/v1/messages',
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-type': 'application/json',
            'Accept': 'application/json'
        },
        data:request.data
    }).handler(200, function(message) {
        showText(window.location.protocol + '//' + window.location.host + 
            '#' + message.id);
    }).handler(-200, function() {
        showText('Se produjo un error');
    });
});


zvent.subscribe(/^([0-9a-f]{8})$/, function(request, id) {
    showText('Cargando...');
    ajax({
        url: '/api-rest/v1/messages/' + id,
        headers: {
            'Accept': 'application/json'
        }
    }).handler(200, function(message) {
        showText('Si cerras o actualizas no volverás a ver este mensaje', 
            message.text || 'El mensaje esta vacío');
    }).handler(404, function() {
        showText('El mensaje no existe. <a href="#">Volver</a>');
    }).handler([-200, -404], function() {
        showText('Se produjo un error');
    });
});

zvent.GET(window.location.hash);
