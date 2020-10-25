import React, { useState, useEffect } from 'react';
import debounce from 'lodash/debounce';

import { Socket } from './Socket';

import './MessageForm.css';

export default function MessageForm() {
    const [userName, setUserName] = useState('');
    const [picUrl, setPicUrl] = useState('');
    const [state, setState] = useState(true);
    const [isTyping, setIsTyping] = useState(false);

    // Shows when the current user is typing
    const handleTyping = debounce(() => {
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
            setUserName(data.userName);
            setPicUrl(data.picUrl);
            setState(false);
        });
    }, []);

    // Handles form submit- get message value and emit it via socket
    function handleSubmit(event) {
        const newMessage = document.getElementById('text').value;

        Socket.emit('new message', {
            message: newMessage,
            userName,
            picUrl,
        });

        document.getElementById('text').value = '';
        event.preventDefault();
    }

    // Handle logout button
    function handleLogout(event) {
        Socket.emit('logout');
        setState(true);
        event.preventDefault();
    }

    const name = JSON.stringify(userName).replace(/"/g, '');

    return (
        <div>
            <div className="outer">
                <p>{isTyping && `${name} is typing...`}</p>
            </div>
            <form className="formContainer" onSubmit={handleSubmit} autoComplete="off">
                <div className="inputContainer">
                    <input type="text" id="text" placeholder="Enter yer message..." disabled={state} onChange={handleChange} />
                </div>
                <div className="buttonContainer">
                    <button type="submit" disabled={state}>
                        Send
                        <br />
                        Message
                    </button>
                </div>
                <div className="buttonContainer">
                    <button type="submit" className="logout" onClick={handleLogout} disabled={state}>Logout</button>
                </div>
            </form>
        </div>
    );
}
