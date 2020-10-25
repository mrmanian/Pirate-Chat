import React from 'react';

import FacebookLogin from 'react-facebook-login/dist/facebook-login-render-props';
import { FacebookLoginButton } from 'react-social-login-buttons';
import { Socket } from './Socket';

export default function FacebookButton() {
    function handleSubmit(response) {
        const { name } = response;
        const picUrl = response.picture.data.url;
        Socket.emit('new facebook user', {
            name,
            picUrl,
        });
    }

    function handleFailure() {
        return (null);
    }

    return (
        <FacebookLogin
            appId="1218688188501565"
            autoLoad={false}
            fields="name,picture"
            callback={handleSubmit}
            onFailure={handleFailure}
            render={(renderProps) => (
                <FacebookLoginButton onClick={renderProps.onClick} />
            )}
        />
    );
}
