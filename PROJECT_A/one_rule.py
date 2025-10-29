import Orange
import numpy as np

"""
WARNING:
The following one rule algorithm will classify for discrete datasets only 
"""

def one_rule(data):
    """
    Simple 1-Rule learner.
    Receives an Orange.data.Table and returns:
      - best_feature: the attribute with lowest error
      - rule: dict mapping feature value -> predicted class
      - error_rate: fraction of misclassified instances on training data
    """
    domain = data.domain
    class_var = domain.class_var
    # classes = list(class_var.values)

    best_feature = None
    best_rule = None
    best_error = np.inf

    for feature in domain.attributes:
        if feature.is_continuous:
            continue

        # Build rule for this feature
        rule = {}
        errors = 0

        for val in feature.values:
            # Select rows where this feature == val
            subset = [inst for inst in data if inst[feature] == val]
            if len(subset) == 0:
                continue

            # Count class frequencies in this subset
            freq = {}
            for inst in subset:
                cls = inst.get_class()
                try:
                    cls_key = cls.value if hasattr(cls, 'value') else cls
                    freq[cls_key] = freq.get(cls_key, 0) + 1
                except TypeError:
                    cls_key = str(cls)
                    freq[cls_key] = freq.get(cls_key, 0) + 1

            maj_class = max(freq, key=freq.get)
            
            rule[str(val)] = maj_class

            errors += len(subset) - freq[maj_class]

        error_rate = errors / len(data)

        if error_rate < best_error:
            best_error = error_rate
            best_feature = feature
            best_rule = rule

    return best_feature, best_rule, best_error

    # predicted_class = rule[instance[best_feature]]

