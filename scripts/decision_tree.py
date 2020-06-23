from collections import Counter
import unittest
import math
import random

class DecisionTree(object):
    """
        Class of the Decision Tree
    """
    def __init__(self):
        self.root = None

    def stopping_cond(self, records):
        """
        The stopping_cond() function is used to terminate the tree-growing
        process by testing whether all the records have either the same class
        label or the same attribute values.
        This function should return True/False to indicate whether the stopping
        criterion is met.
        """
        # Your code here
        firstRowLabel = records[0]["label"]
        for row in records:
            if (row["label"] != firstRowLabel):  # if there is no label it return false else true
                return False
        return True

    def classify(self, records, col, val):
        """
        This function determines the class label to be assigned to a leaf node.
        For each node t, let p(i|t) denote the fraction of training records from
        class i associated with the node t. In most cases, the leaf node is
        assigned to the class that has the majority number of training records
        This function should return a label that is assigned to the node
        """

        # Count the labels and return the majority label
        left_records = []
        right_records = []
        for row in records:
            if row["attributes"][col] == val:
                left_records.append(row)
            else:
                right_records.append(row)
        return (left_records, right_records)


    def entropy(self, records):
        """
        This function calculates the entropy of given set of records
        """
        positive_label_length = 0.0
        negative_label_length = 0.0
        for row in records:
            if row["label"] == "positive":
                positive_label_length += 1
            else:
                negative_label_length += 1
        records_length = positive_label_length + negative_label_length
        if positive_label_length == 0.0 or negative_label_length == 0.0:
            return_value = 0.0
        else:
            positive_ratio = positive_label_length / records_length
            negative_ratio = negative_label_length / records_length
            return_value = -1.0 * ((positive_ratio) * math.log(positive_ratio, 2) + (negative_ratio) * math.log(negative_ratio, 2))
        return return_value


    def find_best_split(self, records, attributes):
        """
        The find_best_split() function determines which attribute should be
        selected as the test condition for splitting the training records.
        The test condition should be measured by Gain Ratio.
        This function should return multiple information:
        attributed selected for splitting,
        threshold value for splitting,
        best_gain_ratio,
        left subset,
        right subset
        """

        # Your code here
        # Hint-1: loop through all available attributes
        # Hint-2: for each attribute, loop through all possible values
        # Hint-3: calculate gain ratio and pick the best attribute

            # Split the records into two parts based on the value of the select
            # attribute

                # calculate the information gain based on the new split

                # calculate the gain ratio

                # if the gain_ratio is better the best split we have tested
                # set this split as the best split
        node = {}
        attribute_index = 0
        attribute_value = 'x'
        best_gain = 0.0
        left_subset = []
        right_subset = []

        for col in attributes:
            columnvalues = {}
            for row in records:
                columnvalues[row["attributes"][col]] = '1'
            for val in columnvalues:
                (left_records, right_records) = self.classify(records, col, val)
                left_entropy = self.entropy(left_records)
                right_entropy = self.entropy(right_records)
                records_entropy = self.entropy(records)
                records_length = float(len(records))
                leftrecord_length = float(len(left_records))
                rightrecord_length = float(len(right_records))
                left_ratio = leftrecord_length / records_length
                right_ratio = rightrecord_length / records_length
                current_gain = records_entropy - ((left_ratio * left_entropy) + (right_ratio * right_entropy))
                if(current_gain > best_gain):
                    best_gain = current_gain
                    left_subset = left_records
                    right_subset = right_records
                    attribute_index = col
                    attribute_value = val
                    node["attribute_index"] = col
                    node["attribute_value"] = val
        return (attribute_index, attribute_value, best_gain, left_subset, right_subset, node)


    def train(self, records, attributes):
        """
            This function trains the model with training records "records" and
            attribute set "attributes", the format of the data is as follows:
                records: training records, each record contains following fields:
                    label - the lable of this record
                    attributes - a list of attribute values
                attributes: a list of attribute indices that you can use for
                            building the tree
            Typical data will look like:
                records: [
                            {
                                "label":"p",
                                "attributes":['p','x','y',...]
                            },
                            {
                                "label":"e",
                                "attributes":['b','y','y',...]
                            },
                            ...]
                attributes: [0, 2, 5, 7,...]
        """
        records_75 = random.sample(records,int(len(records)))
        self.root = self.tree_growth(records_75,attributes)

    def tree_growth(self, records, attributes):
        """
        This function grows the Decision Tree recursively until the stopping
        criterion is met. Please see textbook p164 for more details
        This function should return a TreeNode
        """
        # Your code here
        # Hint-1: Test whether the stopping criterion has been met by calling function stopping_cond()
        # Hint-2: If the stopping criterion is met, you may need to create a leaf node
        # Hint-3: If the stopping criterion is not met, you may need to create a
        #         TreeNode, then split the records into two parts and build a
        #         child node for each part of the subset
        (attribute_index, attribute_value, best_gain, left_subset, right_subset, node) = self.find_best_split(records,attributes)
        if best_gain == 0.0:
            positive_label = 0.0
            negative_label = 0.0
            for row in records:
                if row["label"] == "positive":
                    positive_label += 1
                else:
                    negative_label += 1
            if(positive_label > negative_label):
                node = {"label":"positive"}
            else:
                node = {"label":"negative"}
        else:
            if self.stopping_cond(left_subset):
                node["left"] = {"label": left_subset[0]["label"]}
            else:
                node["left"] = self.tree_growth(left_subset, attributes)
            if self.stopping_cond(right_subset):
                node["right"] = {"label": right_subset[0]["label"]}
            else:
                node["right"] = self.tree_growth(right_subset, attributes)
        return node

    def predict(self, sample):
        """
        This function predict the label for new sample by calling the predict
        function of the root node
        """
        #return self.root.predict(sample)
        current_node = self.root
        is_not_leaf_node = True
        while is_not_leaf_node:
            if(current_node.get("label") == None):
                attribute_index = current_node["attribute_index"]
                attribute_value = current_node["attribute_value"]
                if sample["attributes"][attribute_index] == attribute_value:
                    current_node = current_node["left"]
                else:
                    current_node = current_node["right"]
            else:
                is_not_leaf_node = False
        return current_node["label"]



if __name__ == "__main__":
    unittest.main()