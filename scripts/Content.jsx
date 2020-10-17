import React, { useState, useEffect } from 'react';

import { Users } from './Users';
import { MessageForm } from './MessageForm';
import { Socket } from './Socket';

import './Content.css';

export function Content() {
    const [messages, setMessages] = useState([]);
    
// Gets message via socket
    useEffect(() => {
        Socket.on('messages received', updateMessages);
        return () => {
            Socket.off('messages received', updateMessages);
        };
    });
    
// Update hook with the new messages
    function updateMessages(data) {
        console.log('Received messages from the server: ' + data['allMessages']);
        setMessages(data['allMessages']);
    }
    
// Creates chat box and message content
    return (
        <div>
            <div className='outerContainer'>
                <div className='topContainer'>
                    <Users />
                </div>
                <div className='container'>
                    <ul>
                        {messages.map((message, index) => (
                        <li className='list' key={index}>{message}</li>))}
                    </ul>
                </div>
                <MessageForm />
            </div>
        </div>
    );
}
