import React from 'react';

import { Socket } from './Socket';

function getMessage() {
    let mess = document.getElementById('text').value;

    Socket.emit('new message', {
        'message': mess,
    });
    
    console.log('Sent the message ' + mess + ' to server!');
}

function handleSubmit(event) {
    event.preventDefault();
    document.getElementById('text').value = '';
}

export function Button() {
    return (
        <form onSubmit={handleSubmit} autocomplete="off">
            <input type="text" id="text" />
            <button type="submit" onClick={getMessage}>Send Message</button>
        </form>
    );
}