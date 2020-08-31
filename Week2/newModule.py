import utils as myUtils

# Test 1
print("test 1")
outputFileName = "outputFile1.txt"
myUtils.first_function("./", outputFileName);

# Test 2
print("test 2")
outputFileName = "outputFile2.txt"
myUtils.second_function("./", outputFileName);

# Test 3
print("test 3")
lst_files = ["./subfolder/file1.txt", "./subfolder/file2.txt"]
myUtils.third_function(lst_files);

# Test 4
print("test 4")
lst_files = ["./subfolder/file1.txt", "./subfolder/file2.txt"]
myUtils.fourth_function(lst_files);

# Test 5
print("test 5")
outputFileName = "outputFile5.txt"
lst_files = ["./subfolder/README.md", "./subfolder/README_TOO.md"]
myUtils.fifth_function(lst_files, outputFileName);