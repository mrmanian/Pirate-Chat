import React, { useState, useEffect } from 'react';

import { Socket } from './Socket';

import './MessageForm.css';

export function MessageForm() {
    const [userName, setUserName] = useState('');
    const [picUrl, setPicUrl] = useState('');
    const [state, setState] = useState(true);

// Set username for each connection
    useEffect(() => {
        Socket.on('userName', (data) => {
            setUserName(data['userName']);
            setPicUrl(data['picUrl']);
            setState(false);
            console.log('Received username: ' + data['userName']);
            console.log('Received profile picture url: ' + data['picUrl']);
        });
    }, []);
    
// Handles form submit- get message value and emit it via socket
    function handleSubmit(event) {
        let newMessage = document.getElementById('text').value;
        
        Socket.emit('new message', {
            'message': newMessage,
            'userName': userName,
            'picUrl': picUrl
        });
        
        console.log('Sent the message "' + newMessage + '" to server!');
        console.log('Sent the username "' + userName + '" to server!');
        console.log('Sent the profile pic url "' + picUrl + '" to server!');
        
        document.getElementById('text').value = '';
        event.preventDefault();
    }

// Creates input box and button
    return (
        <form className='formContainer' onSubmit={handleSubmit} autoComplete='off'>
            <div className="inputContainer">
                <input type='text' id='text' placeholder='Enter yer message...' disabled={state}></input>
            </div>
            <div className="buttonContainer">
                <button type='submit' disabled={state}>Send<br/>Message</button>
            </div>
        </form>
    );
}
