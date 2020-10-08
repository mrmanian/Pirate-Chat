import React from 'react';

import { Socket } from './Socket';

function handleSubmit(event) {
    let newMessage = document.getElementById('text').value;

    Socket.emit('new message', {
        'message': newMessage,
    });
    
    console.log('Sent the message "' + newMessage + '" to server!');
    
    document.getElementById('text').value = '';
    event.preventDefault();
}

export function Button() {
    return (
        <form onSubmit={handleSubmit} autoComplete="off">
            <input type="text" id="text" placeholder="Type your message..."></input>
            <button type="submit">Send Message</button>
        </form>
    );
}
