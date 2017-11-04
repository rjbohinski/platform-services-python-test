# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

from handlers.rewards_handler import RewardsHandler
from handlers.order_handler import OrderHandler
from handlers.customer_handler import CustomerHandler

url_patterns = [
    (r'/rewards/?', RewardsHandler),
    (r'/order/?', OrderHandler),
    (r'/customer/?', CustomerHandler)
]
