import Orange

# Load CSV
data = Orange.data.Table("dataset_long_name_ORIGINAL.csv")

# Save as TAB
data.save("dataset_long_name_CONVERTED.tab")