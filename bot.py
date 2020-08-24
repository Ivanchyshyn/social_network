import configparser
import random
import string

import requests

API_URL = 'http://localhost:5000/api'
SIGN_UP_URL = API_URL + '/sign-up'
CREATE_POST_URL = API_URL + '/post'
LIKE_POST_URL_FMT = API_URL + '/post/{post_id}/like'

EMAIL_DOMAINS = [f'{letter}.com' for letter in string.ascii_lowercase]
EMAIL_LETTERS = string.ascii_lowercase
PASSWORD_LETTERS = string.printable


def main(number_of_users=1, max_posts_per_user=1, max_likes_per_user=1):
    # set function arguments as of 1 and higher (discard 0 and negative numbers)
    number_of_users = max(1, number_of_users)
    max_posts_per_user = max(1, max_posts_per_user)
    max_likes_per_user = max(1, max_likes_per_user)

    user_sessions = [requests.Session() for _ in range(number_of_users)]

    users = create_users(user_sessions)
    post_ids = create_posts(user_sessions, max_posts_per_user)
    like_posts(user_sessions, post_ids, max_likes_per_user)

    for session in user_sessions:
        session.close()


def create_users(user_sessions):
    users = []
    for user_session in user_sessions:
        username_length = 3

        tries = 10
        password = get_random_password()
        while tries:
            data = {'email': get_random_email(username_length), 'password': password}
            print('data user', data)
            response = user_session.post(SIGN_UP_URL, json=data)
            result = response.json()
            if result['result']:
                break

            tries -= 1
            username_length += 1
        else:
            raise RuntimeError('Can not create a user')

        result = result['data']
        access_token = result['access_token']
        user_session.headers['Authorization'] = f'Bearer {access_token}'

        users.append(result['user'])

    return users


def create_posts(user_sessions, max_posts_per_user):
    post_ids = []
    for user_session in user_sessions:
        posts_per_user = random.randint(1, max_posts_per_user)
        print('post per user', posts_per_user)
        for _ in range(posts_per_user):
            response = user_session.post(CREATE_POST_URL, json={'text': get_random_password()})
            result = response.json()
            if not result['result']:
                continue
            post_ids.append(result['data']['id'])
    return post_ids


def like_posts(user_sessions, post_ids, max_likes_per_user):
    for user_session in user_sessions:
        post_ids_copy = post_ids[:]
        random.shuffle(post_ids_copy)
        likes_per_user = random.randint(1, max_likes_per_user)
        print('likes', likes_per_user, post_ids_copy)
        for _ in range(likes_per_user):
            if not post_ids_copy:
                break

            post_id = post_ids_copy.pop()
            user_session.post(LIKE_POST_URL_FMT.format(post_id=post_id))


def get_random_email(n=16):
    username = ''.join(random.sample(EMAIL_LETTERS, n))
    domain = random.choice(EMAIL_DOMAINS)
    return f'{username}@{domain}'


def get_random_password(n=16):
    return ''.join(random.sample(PASSWORD_LETTERS, n))


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('bot_config.ini')
    config = config['DEFAULT']

    _users = int(config['number_of_users'])
    _posts = int(config['max_posts_per_user'])
    _likes = int(config['max_likes_per_user'])

    main(_users, _posts, _likes)
