import React from 'react';
import ReactDOM from 'react-dom';

import FacebookLogin from 'react-facebook-login/dist/facebook-login-render-props';
import { FacebookLoginButton } from 'react-social-login-buttons';
import { Socket } from './Socket';

export function FacebookButton() {
    function handleSubmit(response) {
        let name = response.name;
        let picUrl = response.picture.data.url;
        Socket.emit('new facebook user', {
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
        <FacebookLogin
            appId='1218688188501565'
            autoLoad={false}
            fields='name,picture'
            callback={handleSubmit}
            onFailure={handleFailure}
            render={renderProps => (
                <FacebookLoginButton onClick={renderProps.onClick}></FacebookLoginButton>
            )}
        /> 
    );
}
