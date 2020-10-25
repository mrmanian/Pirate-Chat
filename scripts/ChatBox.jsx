import React, { useState, useEffect } from 'react';
import Linkify from 'react-linkify';

import { Socket } from './Socket';

import './ChatBox.css';

export default function ChatBox() {
    const [userNames, setUserNames] = useState([]);
    const [picUrls, setPicUrls] = useState([]);
    const [messages, setMessages] = useState([]);

    // Display links on new page
    const componentDecorator = (href, text, key) => (
        <a href={href} key={key} target="_blank" rel="noopener noreferrer">
            {text}
        </a>
    );

    // Update hook with the new data
    function updateData(data) {
        setUserNames(data.allUserNames);
        setPicUrls(data.allPicUrls);
        setMessages(data.allMessages);
    }

    // Gets message via socket
    useEffect(() => {
        Socket.on('messages received', updateData);
        return () => {
            Socket.off('messages received', updateData);
        };
    }, []);

    // Check if message is an image or a link
    function checkIsImgOrLink(data) {
        if (data.indexOf('.jpg') !== -1) {
            return (<img className="images" src={data} alt="Invalid pic link" />);
        }
        if (data.indexOf('.png') !== -1) {
            return (<img className="images" src={data} alt="Invalid pic link" />);
        }
        if (data.indexOf('.gif') !== -1) {
            return (<img className="images" src={data} alt="Invalid pic link" />);
        }

        return (
            <Linkify componentDecorator={componentDecorator}>
                {data}
            </Linkify>
        );
    }

    return (
        <ul>
            {messages.map((message, index) => (
                <li className="list" key={index.id}>
                    <img className="profilePic" src={picUrls[index]} alt="Invalid pic link" />
                    {' '}
                    {userNames[index]}
                    :
                    {' '}
                    {checkIsImgOrLink(message)}
                </li>
            ))}
        </ul>
    );
}
