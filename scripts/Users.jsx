import React, { useState, useEffect } from 'react';

import { Socket } from './Socket';

import './Users.css';

// Counts authenticated users
export default function Users() {
    const [userCount, setUserCount] = useState(0);
    useEffect(() => {
        Socket.on('userConnected', (data) => {
            setUserCount(data.userCount);
        });
    }, []);

    useEffect(() => {
        Socket.on('userDisconnected', (data) => {
            setUserCount(data.userCount);
        });
    }, []);

    return (
        <div>
            <h1>Ahoy, Matey!</h1>
            <h3>
                Number o&apos; connected users:
                {' '}
                {userCount}
            </h3>
        </div>
    );
}
