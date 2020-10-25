import React from 'react';

import Users from './Users';
import MessageForm from './MessageForm';
import Login from './Login';
import ChatBox from './ChatBox';

import './Content.css';

// Displays page contents
export default function Content() {
    return (
        <div>
            <Login />
            <div className="outerContainer">
                <div className="topContainer">
                    <Users />
                </div>
                <div className="container">
                    <ChatBox />
                </div>
                <MessageForm />
            </div>
        </div>
    );
}
