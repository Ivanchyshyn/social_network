from src.api import rest
from src.api.resources.activity import UserActivityView
from src.api.resources.analytics import AnalyticsView
from src.api.resources.post import PostView
from src.api.resources.sign_in import SignInView
from src.api.resources.sign_up import SignUpView

rest.add_resource(SignInView, '/sign-in')
rest.add_resource(SignUpView, '/sign-up')

rest.add_resource(PostView, '/post', '/post/<post_id>', '/post/<post_id>/<action>')

rest.add_resource(AnalyticsView, '/analytics')
rest.add_resource(UserActivityView, '/activity', '/activity/<user_id>')
