import pandas as pd

# Create the four lists
list1 = [None, 'Dunne asfaltinlage (TWZOAB)', None, None, None, 'TWZOAB', None, None, '(d)ZOAB']
list2 = [8, 8.0, 7.0, 6.0, 5.0, 8.0, 7.0, 6.0, 12.0]
list3 = [0, 35000.0, 0, 0, 0, 62500.0, 0, 0, 40000.0]
list4 = [0.0526315789, 0.3157894736842105, 0.631578947368421, 0.42105263157894735, 0.42105263157894735, 0.3684210526315789, 0.3157894736842105, 0.2631578947368421, 0.42105263157894735, 0.3684210526315789, 0.42105263157894735, 0.368421, 0.3157894736842105, 0.631578947368421]

# Create a new DataFrame with the four lists as columns
new_row = pd.DataFrame({'col1': [list1], 'col2': [list2], 'col3': [list3], 'col4': [list4]})

# Create an existing DataFrame
existing_df = pd.DataFrame({'col1', 'col2', 'col3', 'col4'})

# Concatenate the two DataFrames
result = pd.concat([existing_df, new_row], ignore_index=True)

print(result)