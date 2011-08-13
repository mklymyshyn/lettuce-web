# -*- coding: utf-8 -*-

from flask import Flask, request

from lettuce_web.drivers.flask import LettuceFlaskTestEnviron
from lettuce_web import absorb


class DummyFlaskDriver(LettuceFlaskTestEnviron):
    def bootstrap(self):
        self.app = Flask(__name__)

        @self.app.route("/")
        def home():
            return 'home page'

        @self.app.route("/subpage/")
        def subpage():
            return 'sub page'

        @self.app.route("/post/", methods=['POST'])
        def post():
            return "\n".join(["%s=%s" % (name, val) \
                        for name, val in request.form.iteritems()])

        super(DummyFlaskDriver, self).bootstrap()


# we should define `webenv_class`, all other bootstrap
# things will be done automatically
absorb.world.webenv_class = DummyFlaskDriver
