# -*- coding: utf-8 -*-
"""
Created on 16 January 2014
Changed on 16 April 2014

Interfaces for models

.. moduleauthor:: joaonrb <joaonrb@gmail.com>
"""
__author__ = "joaonrb"


class IModel(object):
    """
    Interface class for model
    """

    @classmethod
    def param_details(cls):
        """
        Return a dictionary with the parameters for the set parameters and
        a tuple with min, max, step and default value.

        {
            'paramA': (min, max, step, default),
            'paramB': ...
            ...
        }
        """
        raise NotImplementedError

    def set_params(self, **kwargs):
        """
        Set the parameters in the model.

        kwargs can have an arbitrary set of parameters
        """
        raise NotImplementedError

    def get_name(self):
        """
        Get the informative name for the model.
        :return:
        """
        return self.__class__.__name__

    def get_score(self, user, item):
        """
        A score for a user and item that method predicts.
        :param user: id of the user
        :param item: id of the item
        :return:
        """
        raise NotImplementedError

    def fit(self, training_data):
        """

        :param training_data: DataFrame a frame with columns 'user', 'item'
        :return:
        """
        raise NotImplementedError
