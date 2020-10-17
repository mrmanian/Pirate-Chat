import React, { useState, useEffect } from 'react';

import { Users } from './Users';
import { MessageForm } from './MessageForm';
import { Socket } from './Socket';

import './Content.css';

export function Content() {
    const [userNames, setUserNames] = useState([]);
    const [picUrls, setPicUrls] = useState([]);
    const [messages, setMessages] = useState([]);
    
// Gets message via socket
    useEffect(() => {
        Socket.on('messages received', updateData);
        return () => {
            Socket.off('messages received', updateData);
        };
    });
    
// Update hook with the new data
    function updateData(data) {
        console.log('Received usernames from the server: ' + data['allUserNames']);
        console.log('Received picurls from the server: ' + data['allPicUrls']);
        console.log('Received messages from the server: ' + data['allMessages']);
        setUserNames(data['allUserNames']);
        setPicUrls(data['allPicUrls']);
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
                        {userNames.map((user, index) => (
                        <li className='list' key={index}>{picUrls[index]} {user}: {messages[index]}</li>))}
                    </ul>
                </div>
                <MessageForm />
            </div>
        </div>
    );
}
