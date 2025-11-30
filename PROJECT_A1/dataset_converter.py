import Orange

# Load CSV
data = Orange.data.Table("dataset_long_name_ORIGINAL.csv")

# Save as TAB
Orange.data.io.write_table("dataset_long_name_CONVERTED.tab", data)