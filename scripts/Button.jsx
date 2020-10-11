import React, { useState, useEffect } from 'react';

import { Socket } from './Socket';

export function Button() {
    const [userName, setUserName] = useState('');

// Set username for each connection
    useEffect(() => {
        Socket.on('userName', (data) => {
            setUserName(data['userName']);
            console.log('Received user name: ' + data['userName']);
        });
    });
    
// Handles form submit- get message value and emit it via socket
    function handleSubmit(event) {
        let newMessage = document.getElementById('text').value;
    
        Socket.emit('new message', {
            'message': newMessage,
            'userName': userName
        });
        
        console.log('Sent the message "' + newMessage + '" to server!');
        
        document.getElementById('text').value = '';
        event.preventDefault();
    }

// Creates input box and button
    return (
        <form onSubmit={handleSubmit} autoComplete='off'>
            <input type='text' id='text' placeholder='Enter your message...'></input>
            <button type='submit'>Send Message</button>
        </form>
    );
}
