from src.api import rest
from src.api.resources.post import PostView
from src.api.resources.sign_in import SignInView
from src.api.resources.sign_up import SignUpView

rest.add_resource(SignInView, '/sign-in')
rest.add_resource(SignUpView, '/sign-up')

rest.add_resource(PostView, '/post', '/post/<post_id>', '/post/<post_id>/<action>')
