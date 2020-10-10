import React, { useState, useEffect } from 'react';

import { Socket } from './Socket';

export function Users() {
    const [userCount, setUserCount] = useState(0);
    
    useEffect(() => {
    Socket.on("userConnected", (data) => {
      setUserCount(data['userCount']);
        });
    });
    
    useEffect(() => {
    Socket.on("userDisconnected", (data) => {
      setUserCount(data['userCount']);
        });
    });

    return (
        <div>
            <h3>Number of connected users: {userCount} </h3>
        </div>
    );
}