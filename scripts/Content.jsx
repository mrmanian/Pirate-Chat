import React, { useState, useEffect } from 'react';

import { Button } from './Button';
import { Socket } from './Socket';

export function Content() {
    const [messages, setMessages] = useState([]);
    
    function getNewMessages() {
        useEffect(() => {
            Socket.on('messages received', updateMessages)
            return () => {
                Socket.off('messages received', updateMessages);
            }
        });
    }
    
    function updateMessages(data) {
        console.log('Received messages from the server: ' + data['allMessages']);
        setMessages(data['allMessages']);
    }
    
    getNewMessages();
    
    return (
        <div>
            <h1>Messenger</h1>
            <p style={{"border-style": "inset", "width": "40%", "margin": "auto", "padding-bottom": "15px", "margin-bottom": "25px"}}>
                {messages.map((message, index) => (
                <li style={{"list-style-type": "none"}} key={index}>{message}</li>))}
            </p>
            <Button />
        </div>
    );
}
