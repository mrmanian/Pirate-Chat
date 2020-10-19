import React, { useState, useEffect } from 'react';
import { ReactTinyLink } from "react-tiny-link";

import { Socket } from './Socket';

import './ChatBox.css';

export function ChatBox() {
    const [userNames, setUserNames] = useState([]);
    const [picUrls, setPicUrls] = useState([]);
    const [messages, setMessages] = useState([]);

// Gets message via socket
    useEffect(() => {
        Socket.on('messages received', updateData);
        return () => {
            Socket.off('messages received', updateData);
        };
    }, []);
    
// Update hook with the new data
    function updateData(data) {
        console.log('Received usernames from the server: ' + data['allUserNames']);
        console.log('Received picurls from the server: ' + data['allPicUrls']);
        console.log('Received messages from the server: ' + data['allMessages']);
        setUserNames(data['allUserNames']);
        setPicUrls(data['allPicUrls']);
        setMessages(data['allMessages']);
    }
    
// Check if message is an image or a link
    function checkIsImgOrLink(data) {
        console.log(data);
        if (data.indexOf('.jpg') !== -1) {
            return (<img className='images' src={data} />);
        }
        else if (data.indexOf('.png') !== -1) {
            return (<img className='images' src={data} />);
        }
        else if (data.indexOf('.gif') !== -1) {
            return (<img className='images' src={data} />);
        }
        else if (data.indexOf('http') !== -1) {
            return (
                <ReactTinyLink
                    cardSize='small'
                    showGraphic={true}
                    maxLine={2}
                    minLine={1}
                    url={data}
                 />
            );
        }
        else {
            return data;
        }
    }
    
    return (
        <ul>
            {messages.map((message, index) => (
            <li className='list' key={index}><img className='profilePic' src={picUrls[index]} /> {userNames[index]}: {checkIsImgOrLink(message)}</li>))}
        </ul>
    );
}
