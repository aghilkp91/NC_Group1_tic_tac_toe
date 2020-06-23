import random
import math
from collections import Counter
from decision_tree import DecisionTree

class RandomForest(object):
    def __init__(self, tree_num):
        self.tree_num = int(tree_num)
        self.forest = []
        self.record_index_array = []

    def bootstrap(self, records):
        """
        This function bootstrap will return a set of records, which has the same
        size with the original records but with replacement.
        """
        # You code here
        return_records = []
        return_records_index = random.sample(self.record_index_array, len(records))
        for h in range(0, len(records)):
            return_records.append(records[return_records_index[h]])
        return return_records


    def train(self, records, attributes):
        """
        This function will train the random forest, the basic idea of training a
        Random Forest is as follows:
        1. Draw n bootstrap samples using bootstrap() function
        2. For each of the bootstrap samples, grow a tree, with the following
            modification: at each node, randomly sample m of the predictors and
            choose the best split from among those variables
        """
        # Your code here
        for j in range(0, len(records)):
            self.record_index_array.append(j)
        for i in range(0, self.tree_num):
            self.forest.append(DecisionTree())
            ensembler_attributes = random.sample(attributes, 9)
            ensembler_records = self.bootstrap(records)
            self.forest[i].train(ensembler_records, ensembler_attributes)

    def predict(self, sample):
        """
        The predict function predicts the label for new data by aggregating the
        predictions of each tree
        This function should return the predicted label
        """
        # Your code here
        positive_label = 0
        negative_label = 0
        for i in range(0, self.tree_num):
            predicted_value = self.forest[i].predict(sample)
            if(predicted_value == "positive"):
                positive_label += 1
            else:
                negative_label += 1
        if positive_label > negative_label:
            return "positive"
        return "negative"