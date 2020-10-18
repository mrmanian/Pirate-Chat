import React from 'react';
import ReactDOM from 'react-dom';

import GoogleLogin from 'react-google-login';
import { GoogleLoginButton } from 'react-social-login-buttons';
import { Socket } from './Socket';

export function GoogleButton() {
    function handleSubmit(response) {
        let name = response.profileObj.name;
        let picUrl = response.profileObj.imageUrl;
        Socket.emit('new google user', {
            'name': name,
            'picUrl': picUrl
        });
        
        console.log('Sent the name ' + name + ' to server!');
        console.log('Sent the profile picture url ' + picUrl + ' to server!');
    }
    
    function handleFailure() {
        console.log('Failed authentication.');
    }
    
    return (
        <GoogleLogin
            clientId='589283421664-6kvonrml8a1lod7mhtmucru816l5bv20.apps.googleusercontent.com'
            render={renderProps => (
                <GoogleLoginButton onClick={renderProps.onClick} disabled={renderProps.disabled}></GoogleLoginButton>
            )}
            onSuccess={handleSubmit}
            onFailure={handleFailure}
            cookiePolicy={'single_host_origin'}
        />
    );
}
