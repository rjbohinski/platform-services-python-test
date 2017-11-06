# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import logging
from math import floor

from db.rewards import Rewards
from db.mongodb_manager import MongoDBManager


class Customers(object):
    """Class to get rewards information from the database."""

    logger = logging.getLogger("Customers")

    @staticmethod
    def delete(email):
        """Deletes a customers data from the database.

        :param str email: The customer's email.
        """
        try:
            # Python 2
            if not isinstance(email, (unicode, str)):
                raise TypeError('email is not of type unicode or str.')
        except NameError:
            # Python 3
            if not isinstance(email, str):
                raise TypeError('email is not of type str.')

        Customers.logger.debug(
            "Customers.delete(%s)",
            email)
        client = MongoDBManager().get_client()
        database = client["Customers"]
        sel_cust = database.customers.find_one({"email_address": email})
        database.customers.delete_one({"_id": sel_cust})

    @staticmethod
    def get(email):
        """Gets information about a customer from the database.

        :param str email: The customer's email.
        :return: A dictionary containing information about the customer.
        :rtype: dict
        """

        Customers.logger.debug(
            "Customers.delete(%s)",
            email)
        client = MongoDBManager().get_client()
        database = client["Customers"]

        if email is None:
            sel_cust = database.customers.find({})
        else:
            sel_cust = database.customers.find_one({"email_address": email})

        if sel_cust is not None:
            return sel_cust
        else:
            return None

    @staticmethod
    def _clone_customer(db_object):
        return Customers._create_customer(
            db_object["email_address"],
            db_object["reward_points"])

    @staticmethod
    def _create_customer(email, total_spent=0.0):
        """Creates a customer dict.

        :param str email: The customer's email.
        :param float total_spent: The amount of money the customer has spent.
        :return: A dictionary containing information about the customer.
        :rtype: dict
        """
        try:
            # Python 2
            if not isinstance(email, (unicode, str)):
                raise TypeError('email is not of type unicode or str.')
        except NameError:
            # Python 3
            if not isinstance(email, str):
                raise TypeError('email is not of type str.')
        if not isinstance(total_spent, float):
            try:
                total_spent = float(total_spent)
            except ValueError:
                raise TypeError('total_spent is not of type float.')

        current_tier, next_tier = Rewards.get_tier(floor(total_spent))

        reward_tier, reward_tier_name, reward_tier_points = \
            Rewards.get_tier_info(current_tier)
        next_reward_tier, next_reward_tier_name, next_reward_tier_points = \
            Rewards.get_tier_info(next_tier)

        if reward_tier_points is None:
            progress = floor(total_spent) / next_reward_tier_points
        elif next_tier is None:
            progress = None
        else:
            progress = (
                floor(total_spent) - reward_tier_points) / (
                next_reward_tier_points - reward_tier_points)

        customer = {
            "email_address": email,
            "reward_points": floor(total_spent),
            "reward_tier": reward_tier,
            "reward_tier_name": reward_tier_name,
            "next_reward_tier": next_reward_tier,
            "next_reward_tier_name": next_reward_tier_name,
            "next_reward_tier_progress": progress
        }

        return customer

    @staticmethod
    def update(email, total_spent=0.0):
        """Updates an existing database record for a customer.
        The total_spent value is added to the existing total.

        :param str email: The customer's email.
        :param float total_spent: The amount of money the customer has spent.
        :return: A dictionary containing information about the customer.
        :rtype: dict
        """
        try:
            # Python 2
            if not isinstance(email, (unicode, str)):
                raise TypeError('email is not of type unicode or str.')
        except NameError:
            # Python 3
            if not isinstance(email, str):
                raise TypeError('email is not of type str.')
        if not isinstance(total_spent, float):
            try:
                total_spent = float(total_spent)
            except ValueError:
                raise TypeError('total_spent is not of type float.')

        client = MongoDBManager().get_client()
        database = client["Customers"]

        sel_cust = database.customers.find_one({"email_address": email})
        total_spent += sel_cust["reward_points"]

        customer = Customers._create_customer(email, total_spent)

        database.customers.update_one(
            {"_id": sel_cust["_id"]},
            {"$set": customer})
        return customer

    @staticmethod
    def insert(email, total_spent=0.0):
        """Creates a database record for a new customer.

        :param str email: The customer's email.
        :param float total_spent: The amount of money the customer has spent.
        :return: A dictionary containing information about the customer.
        :rtype: dict
        """
        try:
            # Python 2
            if not isinstance(email, (unicode, str)):
                raise TypeError('email is not of type unicode or str.')
        except NameError:
            # Python 3
            if not isinstance(email, str):
                raise TypeError('email is not of type str.')
        if not isinstance(total_spent, float):
            try:
                total_spent = float(total_spent)
            except ValueError:
                raise TypeError('total_spent is not of type float.')

        Customers.logger.debug(
            "Customers.insert(%s, %s)",
            email,
            total_spent)
        client = MongoDBManager().get_client()
        database = client["Customers"]
        customer = Customers._create_customer(email, total_spent)
        database.customers.insert(customer)
        return customer

    @staticmethod
    def auto_insert_update(email, total_spent=0.0):
        """Either creates or updates a database record for a customer.

        :param str email: The customer's email.
        :param float total_spent: The amount of money the customer has spent.
        :return: A dictionary containing information about the customer.
        :rtype: dict
        """
        try:
            # Python 2
            if not isinstance(email, (unicode, str)):
                raise TypeError('email is not of type unicode or str.')
        except NameError:
            # Python 3
            if not isinstance(email, str):
                raise TypeError('email is not of type str.')
        if not isinstance(total_spent, float):
            try:
                total_spent = float(total_spent)
            except ValueError:
                raise TypeError('total_spent is not of type float.')

        client = MongoDBManager().get_client()
        database = client["Customers"]
        search_query = database.customers.find({"email_address": email})
        customer = None
        if search_query is None or search_query.count() == 0:
            customer = Customers.insert(email, total_spent)
        else:
            if search_query.count() > 1:
                Customers.logger.warning(
                    "Multiple database entries found for \"%s\", "
                    "still attempting to update.",
                    email)
            customer = Customers.update(email, total_spent)

        return customer
