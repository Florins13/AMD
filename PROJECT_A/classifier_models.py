import Orange
from one_rule import one_rule  # your existing one_rule() function


class OrangeClassifierManager:
    def __init__(self, dataset_name="dataset.tab", split_ratio=0.8):
        """
        Handles data loading, splitting, and provides train/test sets
        for multiple classifiers (including custom ones).
        """
        # Load dataset
        self.data = Orange.data.Table(dataset_name)

        print(f"Loaded dataset: {dataset_name}")
        print("Domain:", self.data.domain)
        print("Instances:", len(self.data))

        # Split into training/testing sets
        self.train, self.test = Orange.evaluation.testing.sample(self.data, n=split_ratio)

        print(f"{len(self.train)} training examples")
        print(f"{len(self.test)} testing examples")

    # --------------------------
    # One Rule Classifier
    # --------------------------
    def one_rule_model(self):
        best_feature, best_rule, best_error = one_rule(self.train)

        # Evaluate on test set
        errors = 0
        for inst in self.test:
            # must convert value object from orange framework to string to work
            val = str(inst[best_feature])
            pred = str(best_rule.get(val, None))
            if pred != inst.get_class():
                errors += 1

        test_error_rate = errors / len(self.test)
        print(f"[1-Rule] Test error rate: {test_error_rate:.2f}")

        return best_feature, best_rule, best_error, test_error_rate

    # --------------------------
    # Induction tree classifier
    # --------------------------    
    def induction_tree_model(self):
        learner = Orange.classification.TreeLearner()
        classifier = learner(self.train) 
        
        errors = 0
        for inst in self.test:
            pred = classifier(inst)
            if pred != inst.get_class():
                errors += 1
        
        test_error_rate = errors / len(self.test)
        print(f"[Decision Tree] Test error rate: {test_error_rate:.2f}")
        return test_error_rate


    # --------------------------
    # Naive Bayes Classifier
    # --------------------------
    def naive_bayes_model(self):
        learner = Orange.classification.NaiveBayesLearner()
        classifier = learner(self.train)

        errors = 0
        for inst in self.test:
            pred = classifier(inst)
            if pred != inst.get_class():
                errors += 1
        test_error_rate = errors / len(self.test)
        print(f"[Naive Bayes] Test error rate: {test_error_rate:.2f}")

        return test_error_rate

if __name__ == "__main__":
    print("=== Running One Rule Classifier ===")
    manager = OrangeClassifierManager("dataset.tab")
    best_feature, best_rule, best_error, test_error_rate = manager.one_rule_model()

    manager.induction_tree_model()
    manager.naive_bayes_model()

    # print("\n=== One Rule Classifier Results Summary ===")
    # print(f"Best feature: {best_feature.name}")
    # print(f"Training error rate: {best_error:.2f}")
    # print(f"Testing error rate:  {test_error_rate:.2f}")

    # count = 0

    # for i in range(0, 50): # edit the number of instances to be shown on print
    #     count += 1
    #     # Convert feature value to string to use as dictionary key 
    #     predicted_class = best_rule[str(manager.data[i][best_feature])]
    #     print(f"One Rule model: row {count} with the best feature: {best_feature} with a predicted class: {predicted_class}")
