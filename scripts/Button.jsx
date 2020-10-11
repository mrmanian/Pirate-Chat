import React, { useState, useEffect } from 'react';

import { Socket } from './Socket';

import './Button.css';

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
        <form className='formContainer' onSubmit={handleSubmit} autoComplete='off'>
            <div className="inputContainer">
                <input type='text' id='text' placeholder='Enter your message...'></input>
            </div>
            <div className="buttonContainer">
                <button type='submit'>Send Message</button>
            </div>
        </form>
    );
}
