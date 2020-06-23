import argparse
from DecisionTree import DecisionTree
from RandomForest import RandomForest

def load_data(file_path):
    """
    Load data from given file path, please see data description for details
    of the data format
    """
    records = []
    file = open(file_path)
    for line in file:
        tokens = line.strip().split(',')
        records.append({"label":tokens[9], "attributes":tokens[0:9]})
    attributes = range(len(records[0]["attributes"]))
    #print (records[0]["attributes"][0])
    file.close()
    return records, attributes

def test_model(model, training_file_path):
    """
    Test the accuracy of given model
    """
    records, attributes = load_data(training_file_path)
    model.train(records, attributes)
    test_records = load_data(testing_file_path)[0]
    correct_cnt = 0
    for sample in test_records:
        if model.predict(sample) == sample["label"]:
            correct_cnt += 1
    print ("Accuracy : " + str((float(correct_cnt) * 100) / len(test_records)) + " %")

def main():
    """
    Process the input arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model', default="0")
    parser.add_argument('-t', '--training', default="data/tic_tac_toe_train.data")
    parser.add_argument('-n', '--tree_nums', default=20)
    args = parser.parse_args()

    if args.model == "0":
        print ("Testing Decision Tree model")
        model = DecisionTree()
    else:
        print ("Testing Random Forest model")
        model = RandomForest(args.tree_nums)

    test_model(model, args.training)

if __name__ == "__main__":
    main()
