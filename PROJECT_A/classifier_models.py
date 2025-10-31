import Orange
from one_rule import one_rule


class OrangeClassifierManager:
    def __init__(self, dataset_name="dataset.tab", split_ratio=0.8):
        # Load dataset
        self.data = Orange.data.Table(dataset_name)

        print(f"Loaded dataset: {dataset_name}")
        print("Domain:", self.data.domain)
        print("Instances:", len(self.data))

        # Split into training/testing sets
        self.train, self.test = Orange.evaluation.testing.sample(self.data, n=split_ratio)

        print(f"{len(self.train)} training examples")
        print(f"{len(self.test)} testing examples")

    # One Rule Classifier
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

    # Induction tree classifier  
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


    # Naive Bayes Classifier
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

    # Train all models and return classifiers
    def train_all_models(self):
        # One Rule
        best_feature, best_rule, best_error, one_rule_error = self.one_rule_model()
        
        # Decision Tree
        tree_learner = Orange.classification.TreeLearner()
        tree_classifier = tree_learner(self.train)
        tree_error = self.induction_tree_model()
        
        # Naive Bayes
        nb_learner = Orange.classification.NaiveBayesLearner()
        nb_classifier = nb_learner(self.train)
        nb_error = self.naive_bayes_model()
        
        classifiers = {
            'one_rule': (best_feature, best_rule),
            'tree': tree_classifier,
            'naive_bayes': nb_classifier
        }
        
        error_rates = {
            'one_rule': one_rule_error,
            'tree': tree_error,
            'naive_bayes': nb_error
        }
        
        return classifiers, error_rates
    
    # Predict from user input
    def predict_from_input(self, classifiers, age, prescription, astigmatic, tear_rate):
        # Create an Orange instance from input
        instance = Orange.data.Instance(self.data.domain, [age, prescription, astigmatic, tear_rate, None])
        
        results = {}
        
        # One Rule prediction
        best_feature, best_rule = classifiers['one_rule']
        val = str(instance[best_feature])
        results['One Rule'] = best_rule.get(val, "none")
        
        # Decision Tree prediction
        tree_pred = classifiers['tree'](instance)
        results['Decision Tree'] = self.data.domain.class_var.values[int(tree_pred)]
        
        # Naive Bayes prediction
        nb_pred = classifiers['naive_bayes'](instance)
        results['Naive Bayes'] = self.data.domain.class_var.values[int(nb_pred)]
        
        return results


def interactive_prediction():
    print("=" * 60)
    print("LENS PREDICTION SYSTEM")
    print("=" * 60)
    
    # Train models
    orange_manager = OrangeClassifierManager("dataset.tab")
    classifiers, error_rates = orange_manager.train_all_models()
    
    print("\n" + "=" * 60)
    print("Models trained! Ready for predictions.")
    print("=" * 60)
    
    while True:
        print("\n" + "-" * 60)
        print("Enter patient data (or 'quit' to exit)")
        print("-" * 60)
        print("\nFormat: age,prescription,astigmatic,tear_rate")
        print("Example: young,myope,yes,normal")
        print("\nValid values:")
        print("  age: young, pre-presbyopic, presbyopic")
        print("  prescription: myope, hypermetrope")
        print("  astigmatic: yes, no")
        print("  tear_rate: normal, reduced")
        print("-" * 60)
        
        user_input = input("\nEnter data: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("\nThank you for using the Lens Recommendation System!")
            break
        
        try:
            # Parse input
            parts = [p.strip() for p in user_input.split(',')]
            if len(parts) != 4:
                print("Error: Please enter exactly 4 values separated by commas.")
                continue
            
            age, prescription, astigmatic, tear_rate = parts
            
            # Make predictions
            results = orange_manager.predict_from_input(classifiers, age, prescription, astigmatic, tear_rate)
            
            print("\n" + "=" * 60)
            print("PREDICTIONS:")
            print("=" * 60)
            print(f"Patient: {age}, {prescription}, astigmatic={astigmatic}, tear_rate={tear_rate}")
            print("-" * 60)
            
            # Map display names to internal keys
            model_mapping = {
                'One Rule': 'one_rule',
                'Decision Tree': 'tree',
                'Naive Bayes': 'naive_bayes'
            }
            
            for model_name, prediction in results.items():
                model_key = model_mapping[model_name]
                error_rate = error_rates[model_key]
                print(f"  {model_name:20s} → {prediction:10s} (Error Rate: {error_rate:.2%})")
            print("=" * 60)
            
        except Exception as e:
            print(f"Error: {e}")
            print("Please check your input and try again.")


if __name__ == "__main__":
    interactive_prediction()
