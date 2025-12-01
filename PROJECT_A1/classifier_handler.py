import Orange
from one_rule import one_rule

class ClassifierHandler():
    def __init__(self, dataset_name="dataset_long_name_CONVERTED.tab", split_ratio=0.8):
        # Load dataset
        self.data = Orange.data.Table(dataset_name)
        
        # If 'class' is not the class variable, set it manually
        if self.data.domain.class_var is None:
            # Find the 'class' attribute
            class_attr = None
            for attr in self.data.domain.attributes:
                if attr.name == 'class':
                    class_attr = attr
                    break
            
            if class_attr:
                # Create new domain with 'class' as the class variable
                new_attrs = [attr for attr in self.data.domain.attributes if attr.name != 'class']
                new_domain = Orange.data.Domain(new_attrs, class_attr)
                self.data = self.data.transform(new_domain)

        print(f"Loaded dataset: {dataset_name}")
        print("Domain:", self.data.domain)
        print("Instances:", len(self.data))

        # Split into training/testing sets
        self.train, self.test = Orange.evaluation.testing.sample(self.data, n=split_ratio)

        print(f"{len(self.train)} training examples")
        print(f"{len(self.test)} testing examples")

    def apply_one_rule(self):
        #Apply 1R algorithm and generate detailed statistics
        best_feature, best_rule, best_error = one_rule(self.train)
        
        print(f"\nBest feature selected by 1R: {best_feature.name}")
        print(f"Error rate: {best_error:.4f}")
        print(f"Rule: {best_rule}")
        
        return best_feature, best_rule, best_error

    def generate_one_rule_output(self, output_file="oneR_OUTPUT.txt"):
        """
        Generate and save 1R output in the format:
        (attr, valueAttr, valueTarget) : (error, total)
        """
        best_feature, best_rule, best_error = self.apply_one_rule()
        
        class_var = self.train.domain.class_var
        attr_name = best_feature.name
        
        # Collect statistics for each (attr_value, class_value) combination
        stats = {}
        
        for attr_val in best_feature.values:
            # Get all instances with this attribute value
            subset = [inst for inst in self.train if inst[best_feature] == attr_val]
            
            if len(subset) == 0:
                continue
            
            # Get the predicted class for this attribute value from the rule
            predicted_class = best_rule[str(attr_val)]
            
            # Count occurrences for each class value
            for class_val in class_var.values:
                # Count instances with this attr_val and class_val
                count = sum(1 for inst in subset if str(inst.get_class()) == class_val or 
                           (hasattr(inst.get_class(), 'value') and inst.get_class().value == class_val))
                
                if count > 0:
                    # Error count: if predicted class != actual class, all instances are errors
                    error = count if str(predicted_class) != class_val else 0
                    
                    key = (attr_name, str(attr_val), class_val)
                    stats[key] = (error, count)
        
        # Write to file
        with open(output_file, 'w') as f:
            f.write(f"Selected attribute: {attr_name}\n")
            f.write(f"Error rate: {best_error:.4f}\n\n")
            
            for (attr, attr_val, class_val), (error, total) in sorted(stats.items()):
                f.write(f"({attr}, {attr_val}, {class_val}) : ({error}, {total})\n")
        
        print(f"\n1R output saved to {output_file}")
        return stats

if __name__ == "__main__":
    handler = ClassifierHandler(
        dataset_name="dataset_long_name_CONVERTED.tab", 
        split_ratio=0.8
    )
    
    # Apply 1R and generate output file
    handler.generate_one_rule_output("oneR_OUTPUT.txt")