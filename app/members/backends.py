import requests
from django.contrib.auth import get_user_model

from config import settings
User = get_user_model()


class FacebookBackend:
    def authenticate(self, request, code):
        '''
        Facebook의 Authorization Code가 주어졌을 때
        적절히 처리해서
        facebook의 user_id에 해당하는 User가 있으면 해당 User를 리턴
        없으면 생성해서 리턴
        :param request: View의 HttpRequest object
        :param code: Facebook Authorization code
        :return:
        '''

        def get_access_token(code):
            '''
            authorization code를 사용해 엑세스 토큰을 받아옴

            :param code: 유저의 페이스북 인증 후 전달되는 authorization code
            :return: 엑세스 토큰 문자열
            '''
            # GET parameter에 'code'에 값이 전달됨 (authentication code)
            # 전달받은 인증코드를 사용해서 엑세스토큰을 받음

            url = 'https://graph.facebook.com/v3.0/oauth/access_token'
            parmas = {
                'client_id': settings.FACEBOOK_APP_ID,
                'redirect_uri': 'http://localhost:8000/members/facebook-login/',
                'client_secret': settings.FACEBOOK_APP_SECRET_CODE,
                'code': code,
            }
            response = requests.get(url, parmas)
            # response_dict = json.loads(response.text)
            response_dict = response.json()
            access_token = response_dict['access_token']

            return access_token

        def debug_token(token):
            url = 'https://graph.facebook.com/debug_token'
            params = {
                'input_token': token,
                'access_token': '{}|{}'.format(
                    settings.FACEBOOK_APP_ID,
                    settings.FACEBOOK_APP_SECRET_CODE,
                )
            }
            response = requests.get(url, params)
            return response.json()

        # GraphAPI를 통해서 'me'유저의 FaceBook User정보 받아오기
        def get_user_info(token, fields=('id', 'name', 'first_name', 'last_name', 'picture')):
            url = 'https://graph.facebook.com/v3.0/me'

            params = {
                'fields': ','.join(fields),
                'access_token': token,
            }
            response = requests.get(url, params)
            return response.json()

        def create_user_from_facebook_user_info(user_info):
            # 받아온 정보 중 회원가입에 필요한 요소들 꺼내기
            facebook_user_id = user_info['id']
            first_name = user_info['first_name']
            last_name = user_info['last_name']
            url_img_profile = user_info['picture']['data']['url']

            user,user_created = User.objects.get_or_create(username=facebook_user_id,
                                              defaults={
                                                  'first_name': first_name,
                                                  'last_name': last_name,
                                              },
                                              )
            return user, user_created
        access_token = get_access_token(code)
        user_info = get_user_info(access_token)
        user, user_created = create_user_from_facebook_user_info(user_info)

        return user

    def get_user(self, user_id):
        '''
        user_id(primary_key값)이 주어졌을 때,
        해당 User인스턴스가 존재하면 반환하고, 없으면 None값 반환
        :param user_id: User모델의 primary_key값
        :return: primary_key에 해당하는 User가 존재하면 User인스턴스, 아니면 None
        '''
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotexsist:
            return None
