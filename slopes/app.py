from mountaineer.app import AppController
from mountaineer.js_compiler.postcss import PostCSSBundler
from mountaineer.render import LinkAttribute, Metadata


from slopes.controllers.slope import SlopeController
from slopes.controllers.home import HomeController
from slopes.controllers.login import LoginController
from slopes.controllers.logout import LogoutController
from slopes.controllers.signup import SignupController

from slopes.views import get_view_path
from slopes.config import AppConfig
from slopes.models import User

controller = AppController(
    view_root=get_view_path(""),
    config=AppConfig(),
    
    global_metadata=Metadata(
        links=[LinkAttribute(rel="stylesheet", href="/static/app_main.css")]
    ),
    custom_builders=[
        PostCSSBundler(),
    ],
    
)


controller.register(HomeController())
controller.register(SlopeController())
controller.register(LoginController("/"))
controller.register(LogoutController("/"))
controller.register(SignupController("/", User))
