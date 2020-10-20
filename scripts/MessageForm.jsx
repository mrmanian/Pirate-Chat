import React, { useState, useEffect } from 'react';
import debounce from 'lodash/debounce';

import { Socket } from './Socket';

import './MessageForm.css';

export function MessageForm() {
    const [userName, setUserName] = useState('');
    const [picUrl, setPicUrl] = useState('');
    const [state, setState] = useState(true);
    const [isTyping, setIsTyping] = useState(false);
    
// Shows when the current user is typing
    const handleTyping = debounce(function() {
        setIsTyping(false);
    }, 1500);

    useEffect(() => {
        handleTyping();
    }, [isTyping]);
  
    function handleChange() {
        setIsTyping(true);
    }
    
// Set username and profile picture for each connection
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

// Handle logout button
    function handleLogout(event) {
        Socket.emit('logout');
        setState(true);
        event.preventDefault();
    }
    
    var name = JSON.stringify(userName).replace(/\"/g, "");
    
    close();
    return (
        <div>
            <div className='outer'>
                <p>{isTyping && name + ' is typing...'}</p>
            </div>
            <form className='formContainer' onSubmit={handleSubmit} autoComplete='off'>
                <div className='inputContainer'>
                    <input type='text' id='text' placeholder='Enter yer message...' disabled={state} onChange={handleChange}></input>
                </div>
                <div className='buttonContainer'>
                    <button type='submit' disabled={state}>Send<br/>Message</button>
                </div>
                <div className='buttonContainer'>
                    <button className='logout' onClick={handleLogout} disabled={state}>Logout</button>
                </div>
            </form>
        </div>
    );
}
