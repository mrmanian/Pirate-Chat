import React from 'react';

import { GoogleButton } from './GoogleButton';
import { FacebookButton } from './FacebookButton';

import './Login.css';

export function Login() {
    return (
        <div className='loginContainer'>
            <div className='textContainer'>
                <h1>Login to Enter!</h1>
            </div>
            <div className='padding'>
                <GoogleButton />
            </div>
            <div className='padding'>
                <FacebookButton />
            </div>
        </div>
    );
}
