import json

from rauth import OAuth2Service
from flask import redirect, url_for, request

from app.core.config import OAUTH_CREDENTIALS


class OAuth2SignIn:
    def __init__(self, provider_name):
        self.provider_name = provider_name
        self.service = OAuth2Service(
            name=provider_name,
            client_id=OAUTH_CREDENTIALS[provider_name]['id'],
            client_secret=OAUTH_CREDENTIALS[provider_name]['secret'],
            authorize_url=OAUTH_CREDENTIALS[provider_name]['authorize_url'],
            access_token_url=OAUTH_CREDENTIALS[provider_name]['access_token_url'],
            base_url=OAUTH_CREDENTIALS[provider_name]['base_url']
        )

    @classmethod
    def get_provider_class_instance(cls, provider_name):
        for provider_class in cls.__subclasses__():
            provider = provider_class()
            if provider.provider_name == provider_name:
                return provider

    def authorize(self):
        return redirect(
            self.service.get_authorize_url(
                response_type='code',
                display='page',
                redirect_uri=self.get_callback_url()
            )
        )

    def callback(self):
        pass

    def get_callback_url(self):
        return url_for(
            'home.oauth_callback',
            provider=self.provider_name,
            _external=True
        )


class OAuthVKSignIn(OAuth2SignIn):
    def __init__(self):
        super(OAuthVKSignIn, self).__init__('vk')

    def callback(self):
        if 'code' not in request.args:
            return None, None, None

        oauth_session = self.service.get_auth_session(
            data={
                'code': request.args['code'],
                'grant_type': 'authorization_code',
                'redirect_uri': self.get_callback_url()
            },
            decoder=json.loads
        )

        profile = oauth_session.get('users.get?fields=photo_100&v=5.131').json().get('response')[0]

        return (
            'vk_' + str(profile.get('id')),
            profile.get('first_name') + ' ' + profile.get('last_name'),
            profile.get('photo_100')
        )

    def authorize(self):
        return redirect(
            self.service.get_authorize_url(
                response_type='code',
                display='page',
                redirect_uri=self.get_callback_url()
            )
        )


class OAuthGoogleSignIn(OAuth2SignIn):
    def __init__(self):
        super(OAuthGoogleSignIn, self).__init__('google')

    def callback(self):
        if 'code' not in request.args:
            return None, None, None

        oauth_session = self.service.get_auth_session(
            data={
                'code': request.args['code'],
                'grant_type': 'authorization_code',
                'redirect_uri': self.get_callback_url()
            },
            decoder=json.loads
        )

        profile = oauth_session.get('userinfo?alt=json').json()

        return (
            'google_' + profile.get('id'),
            profile.get('given_name') + ' ' + profile.get('family_name'),
            profile.get('picture')
        )

    def authorize(self):
        return redirect(
            self.service.get_authorize_url(
                response_type='code',
                display='page',
                scope='https://www.googleapis.com/auth/userinfo.profile',
                redirect_uri=self.get_callback_url()
            )
        )
