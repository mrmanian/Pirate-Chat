import React, { useState, useEffect } from 'react';

import { Button } from './Button';
import { Socket } from './Socket';

export function Content() {
    const [item, setItem] = React.useState([]);
    
    function newItem() {
        React.useEffect(() => {
            Socket.on('message received', (data) => {
                console.log("Received this message from the server: " + data['item']);
                setItem([...item, data['message']]);
            })
        });
    }
    
    newItem();
    
    return (
        <div>
            <h1>Messenger</h1>
            <p style={{"border-style": "inset", "width": "40%", "margin": "auto", "padding-bottom": "15px", "margin-bottom": "25px"}}>
                {item.map(i => (
                <li style={{"list-style-type": "none"}} key={i}>{i}</li>))}
            </p>
            <Button />
        </div>
    );
}
