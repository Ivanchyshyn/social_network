import concurrent.futures
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


def main(number_of_users=1, max_posts_per_user=1, max_likes_per_user=1, max_threads=1):
    # set function arguments as of 1 and higher (discard 0 and negative numbers)
    number_of_users = max(1, number_of_users)
    max_posts_per_user = max(1, max_posts_per_user)
    max_likes_per_user = max(1, max_likes_per_user)
    max_threads = max(1, max_threads)

    user_sessions = [requests.Session() for _ in range(number_of_users)]

    users = create_users(user_sessions, max_threads=max_threads)
    post_ids = create_posts(user_sessions, max_posts_per_user, max_threads=max_threads)
    like_posts(user_sessions, post_ids, max_likes_per_user, max_threads=max_threads)

    for session in user_sessions:
        session.close()


def create_users(user_sessions, max_threads=1):
    num_of_threads = min(len(user_sessions), max_threads)
    multiple_args = [(user_session,) for user_session in user_sessions]
    users = []

    for result, session in submit_job(send_create_user_request, multiple_args, max_threads=num_of_threads):
        access_token = result['access_token']
        session.headers['Authorization'] = f'Bearer {access_token}'
        users.append(result['user'])

    return users


def create_posts(user_sessions, max_posts_per_user, max_threads=1):
    multiple_args = []
    post_ids = []

    for user_session in user_sessions:
        posts_per_user = random.randint(1, max_posts_per_user)
        print('post per user', posts_per_user)
        _user_posts = [(user_session,)] * posts_per_user
        multiple_args.extend(_user_posts)

    for result in submit_job(send_create_post, multiple_args, max_threads=max_threads):
        post_ids.append(result['id'])

    return post_ids


def like_posts(user_sessions, post_ids, max_likes_per_user, max_threads=1):
    multiple_args = []
    for user_session in user_sessions:
        post_ids_copy = post_ids[:]
        random.shuffle(post_ids_copy)
        likes_per_user = random.randint(1, max_likes_per_user)
        print('likes', likes_per_user)
        for _ in range(likes_per_user):
            if not post_ids_copy:
                break

            post_id = post_ids_copy.pop()
            args = (user_session, post_id)
            multiple_args.append(args)

    for result in submit_job(send_like_post, multiple_args, max_threads=max_threads):
        pass


def send_create_user_request(user_session):
    username_length = 3
    tries = 10
    password = get_random_password()

    while tries:
        data = {'email': get_random_email(username_length), 'password': password}
        print('data user', data)
        try:
            result = send_request(user_session, SIGN_UP_URL, json=data)
            return result, user_session
        except RuntimeError:
            tries -= 1
            username_length += 1
    else:
        raise RuntimeError('Could not create a user')


def send_create_post(user_session):
    return send_request(user_session, CREATE_POST_URL, json={'text': get_random_password()})


def send_like_post(user_session, post_id):
    return send_request(user_session, LIKE_POST_URL_FMT.format(post_id=post_id))


def send_request(session, url, json=None):
    response = session.post(url, json=json)
    result = response.json()
    if not result['result']:
        raise RuntimeError(result.get('error', 'Some error'))
    return result['data']


def submit_job(func, multiple_args, max_threads=None):
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = []
        for args in multiple_args:
            futures.append(executor.submit(func, *args))

        for future in concurrent.futures.as_completed(futures):
            try:
                yield future.result()
            except Exception as exc:
                print(exc)
                continue


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
    _threads = int(config['max_number_of_threads'])

    main(_users, _posts, _likes, _threads)
