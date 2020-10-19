import React from 'react';

import { GoogleButton } from './GoogleButton';
import { FacebookButton } from './FacebookButton';

import './Login.css';

export function Login() {
    return (
        <div className='loginContainer'>
            <h1>Login to Enter</h1>
            <GoogleButton />
            <FacebookButton />
        </div>
    );
}
