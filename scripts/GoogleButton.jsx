import React from 'react';

import GoogleLogin from 'react-google-login';
import { GoogleLoginButton } from 'react-social-login-buttons';
import { Socket } from './Socket';

export default function GoogleButton() {
    function handleSubmit(response) {
        const { name } = response.profileObj;
        const picUrl = response.profileObj.imageUrl;
        Socket.emit('new google user', {
            name,
            picUrl,
        });
    }

    function handleFailure() {
        return (null);
    }

    return (
        <GoogleLogin
            clientId="589283421664-6kvonrml8a1lod7mhtmucru816l5bv20.apps.googleusercontent.com"
            render={(renderProps) => (
                <GoogleLoginButton onClick={renderProps.onClick} disabled={renderProps.disabled} />
            )}
            onSuccess={handleSubmit}
            onFailure={handleFailure}
            cookiePolicy="single_host_origin"
        />
    );
}
