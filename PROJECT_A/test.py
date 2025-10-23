import Orange
from one_rule import one_rule 

# Load an Orange dataset (Titanic is built in)
data = Orange.data.Table("titanic") 

print(type(data))
# <class 'Orange.data.table.Table'>

print(data.domain)
# [sepal length, sepal width, petal length, petal width, class]

print(len(data))
# number of instances (e.g., 150)

# Access all rows (each Instance)
print(data)

best_feature, best_rule, best_error = one_rule(data)

count = 0

# for i in range(0, len(data)):
#     count += 1
#     # Convert feature value to string to use as dictionary key
#     predicted_class = best_rule[str(data[i][best_feature])]
#     print(f"row {count} with the best feature: {best_feature} with a predicted class: {predicted_class}")