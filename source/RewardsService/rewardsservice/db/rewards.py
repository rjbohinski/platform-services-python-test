# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

from operator import itemgetter
import logging

from db.mongodb_manager import MongoDBManager


class Rewards(object):
    """Class to get rewards information from the database."""

    logger = logging.getLogger("Rewards")

    @staticmethod
    def get_tier(points):
        """Converts the points to tier based on the values in the DB.

        :param int points: The number of points earned by the customer.
        :return: The current tier and next tier.
        """
        Rewards.logger.debug("Rewards.get_tier(%s)", points)
        client = MongoDBManager().get_client()
        db = client["Rewards"]
        rewards = list(db.rewards.find({}, {"_id": 0}))
        rewards = sorted(rewards, key=itemgetter("points"))

        if rewards[0]["points"] > points:
            return None, rewards[0]
        elif rewards[-1]["points"] <= points:
            return rewards[-1], None
        else:
            reward_prior = None
            for reward in rewards:
                Rewards.logger.debug(
                    "Reward Prior: %s, Reward: %s", reward_prior, reward)

                if reward_prior is not None:
                    if reward_prior["points"] <= points < reward["points"]:
                        return reward_prior, reward
                reward_prior = reward

    @staticmethod
    def get_tier_info(tier):
        """Simple function that returns the tier, rewardName and points.
        If the supplied tier is None, returns None for all values.

        :param tier: The rewards tier.
        :return: Tier, rewardName, points.
        :raises TypeError: If the supplied tier is not a dict or is not None.
        """
        if not isinstance(tier, dict):
            if tier is None:
                return None, None, None
            else:
                raise TypeError('tier is not of type dict.')

        return tier["tier"], tier["rewardName"], tier["points"]
