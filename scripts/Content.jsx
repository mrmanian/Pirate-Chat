import React, { useState, useEffect } from 'react';
import Linkify from 'react-linkify';

import { Users } from './Users';
import { MessageForm } from './MessageForm';
import { Socket } from './Socket';

import './Content.css';

export function Content() {
    const [userNames, setUserNames] = useState([]);
    const [picUrls, setPicUrls] = useState([]);
    const [messages, setMessages] = useState([]);
    
// Display links on new page
    const componentDecorator = (href, text, key) => (
       <a href={href} key={key} target='_blank' rel='noopener noreferrer'>
         {text}
       </a>
    );

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
    
// Check if message is an image
    function checkIsImg(data) {
        console.log(data);
        if (data.indexOf('.jpg') !== -1) {
            return (<img src={data} />);
        }
        else if (data.indexOf('.png') !== -1) {
            return (<img src={data} />);
        }
        else if (data.indexOf('.gif') !== -1) {
            return (<img src={data} />);
        }
        else {
            return data;
        }
    }
    
// Creates chat box and message content
    return (
        <div>
            <div className='outerContainer'>
                <div className='topContainer'>
                    <Users />
                </div>
                <div className='container'>
                
                <Linkify componentDecorator={componentDecorator}>
                    <ul>
                        {messages.map((message, index) => (
                        <li className='list' key={index}><img src={picUrls[index]} /> {userNames[index]}: {checkIsImg(message)}</li>))}
                    </ul>
                </Linkify>
                </div>
                <MessageForm />
            </div>
        </div>
    );
}
