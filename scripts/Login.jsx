import React from 'react';

import { GoogleButton } from './GoogleButton';

import './Login.css';

export function Login() {
    return (
        <div className='loginContainer'>
            <h1>Login to Enter</h1>
            <GoogleButton />
        </div>
    )
}
