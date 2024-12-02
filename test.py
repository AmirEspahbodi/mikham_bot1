import copy

original_list = [[1, 2, 3], [4, 5, 6]]
shallow_copied_list = copy.copy(original_list)

shallow_copied_list[0][0] = 99
print("Original List:", original_list)
print("Shallow Copied List:", shallow_copied_list)


print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")


original_list = [[1, 2, 3], [4, 5, 6]]
shallow_copied_list = copy.deepcopy(original_list)

shallow_copied_list[0][0] = 199
print("Original List:", original_list)
print("Shallow Copied List:", shallow_copied_list)
