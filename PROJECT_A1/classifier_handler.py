import Orange
from one_rule import one_rule

class ClassifierHandler():
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

    