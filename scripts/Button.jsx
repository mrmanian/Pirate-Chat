import React from 'react';

import { Socket } from './Socket';

// Handles form submit- get message value and emit it via socket
function handleSubmit(event) {
    let newMessage = document.getElementById('text').value;

    Socket.emit('new message', {
        'message': newMessage,
    });
    
    console.log('Sent the message "' + newMessage + '" to server!');
    
    document.getElementById('text').value = '';
    event.preventDefault();
}

// Creates input box and button
export function Button() {
    return (
        <form onSubmit={handleSubmit} autoComplete='off'>
            <input type='text' id='text' placeholder='Enter your message...'></input>
            <button type='submit'>Send Message</button>
        </form>
    );
}
