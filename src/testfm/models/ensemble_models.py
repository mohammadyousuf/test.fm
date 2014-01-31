__author__ = 'linas'

'''
Ensemble models are the ones that take several already built models and combine
them into a single model.
'''



from testfm.models.interface import ModelInterface

class LinearEnsemble(ModelInterface):

    _models = []
    _weights = []

    def __init__(self, models, weights=None):
        '''
        :param models: list of ModelInterface subclasses
        :param weights: list of floats with weights telling how to combine the 
            models
        :return:
        '''

        if weights is not None:
            if len(models) != len(weights):
                raise ValueError("The weights vector length should be the same "
                    "as number of models")

        self._weights = weights
        self._models = models

    def fit(self,training_dataframe):
        pass

    def getScore(self,user,item):
        '''
        :param user:
        :param item:
        :return:
        >>> from testfm.models.baseline_model import IdModel, ConstantModel
        >>> model1 = IdModel()
        >>> model2 = ConstantModel(1.0)
        >>> ensamble = LinearEnsemble([model1, model2], weights=[0.5, 0.5])
        >>> ensamble.getScore(0, 5)
        3.0

        3 because we combine two models in a way: 5 (id of item)*0.5+1(constant
        factor)*0.5

        '''
        predictions = [m.getScore(user, item) for m in self._models]
        return sum([w*p for w,p in zip(self._weights, predictions)])

    def getName(self):
        models = ",".join([m.getName() for m in self._models])
        weights = ",".join(["{:1.4f}".format(w) for w in self._weights])
        return "Linear Ensamble ("+models+"|"+weights+")"


class LogisticEnsemble(ModelInterface):
    '''
    A linear ensemble model which is learned using logistic regression.
    '''

    _user_count = {}

    def getScore(self,user,item):
        x, y = self._extract_features(user, item)
        return float(self.logit.predict(x))

    def getName(self):
        models = ",".join([m.getName() for m in self._models])
        weights = ",".join(["{:1.4f}".format(w) for w in self._weights])
        return "Logistic Ensamble ("+models+"|"+weights+")"

    def __init__(self, models):
        self._models = models

    def _prepare_feature_extraction(self, df):
        '''
        Extracts size of user profile info
        '''
        grouped = df.groupby('user')
        for user, entries in grouped:
            self._user_count[user] = len(entries)

    def _extract_features(self, user, item, relevant=True):
        '''
        Gives proper feature for the logistic function to train on.
        '''

        features = [self._user_count.get(user, 0)]
        features += [m.getScore(user, item) for m in self._models]

        if relevant:
            return features, 1
        else:
            return features, 0

    def prepare_data(self, df):
        from random import choice
        X = []
        Y = []
        items = df.item.unique()
        self._prepare_feature_extraction(df)

        for _, tuple in df.iterrows():
            x, y = self._extract_features(tuple['user'], tuple['item'], relevant=True)
            X.append(x)
            Y.append(y)
            bad_item = choice(items)
            x, y = self._extract_features(tuple['user'], bad_item, relevant=False)
            X.append(x)
            Y.append(y)
        return X, Y

    def fit(self, df):
        from sklearn.linear_model import LogisticRegression

        X, Y = self.prepare_data(df)
        self.logit = LogisticRegression(C=100, penalty='l2', tol=0.01)
        self.logit.fit(X, Y)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
