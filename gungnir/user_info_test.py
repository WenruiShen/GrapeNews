###############################################
#	Testing model.py and its interfaces.
#		Author: 	Wenrui Shen 15210671 Hong Su 15211605
#		Date:		2017-06-19
#		Version:	1.2
#		Description:	Testing Topics_model & News_model: 1st layer API
###############################################
import django
django.setup()
import datetime
# inmport models from your model application
from dataCollector.models import Topics_model,News_model,Medium_model,User_info_model


# test for User_info_model
# test 1 -- test 4.1.1.1
# Test Name: Insert one new user
# Except Output: user's str
print("test 1 -- test 4.1.1.1")
print("Test Name: Insert one new user")
print("Except Output: user's name")
print("Actual Output:")
list1 = [1,2,3,4,5,6,7,8]
list2 = [2,3,4,5,6,7,8,9,10]
user = User_info_model.db_insert_one_new_user("user001","pswd_001")
print(user)



# test for User_info_model
# test 2 -- test 4.1.1.1
# Test Name: Insert one duplicated user
# Except Output: [*] IntegrityError & None"
print("test 2 -- test 4.1.1.1")
print("Test Name: Insert one duplicated user")
print("Except Output: [*] IntegrityError & None")
print("Actual Output:")
list1 = [1,2,3,4,5,6,7,8]
list2 = [2,3,4,5,6,7,8,9,10]
user = User_info_model.db_insert_one_new_user("user001","pswd_001")
print(user)



# test 3 -- test 4.1.1.2
# Test Name: Get one user by its id
# Except Output: user's name
print("test 3 -- test 4.1.1.2")
print("Test Name : Get one user by its id")
print("Except Output: users id & name")
id = 1
print("Actual Output:")
user = User_info_model.db_get_one_user_by_id(id)
print(user.id)
print(user)


# test 4 -- test 4.1.1.2
# Test Name: Get one user by not exist id
# Except Output: [*] IntegrityError & None
print("test 4 -- test 4.1.1.2")
print("Test Name : Get one user by not exist id")
print("Except Output: [*] DoesNotExist & None")
id = 2
print("Actual Output:")
user = User_info_model.db_get_one_user_by_id(id)
print(user)


# test 5 -- test 4.1.1.3
# Test Name: Get one user by its name
# Except Output: user's name
print("test 5 -- test 4.1.1.3")
print("Test Name : Get one user by its name")
print("Except Output: topic's name & id")
print("Actual Output:")
name = "user001"
user = User_info_model.db_get_one_user_by_name(name)
print(user.user_name)
print(user.id)


# test 6 -- test 4.1.1.3
# Test Name: Get one user by not exist name
# Except Output: [*] IntegrityError & None
print("test 6 -- test 4.1.1.3")
print("Test Name : Get one user by not exist name")
print("Except Output: [*] DoesNotExist & None")
print("Actual Output:")
name = "user002"
user = User_info_model.db_get_one_user_by_name(name)
print(user)

# test 7 -- test 4.1.1.4
# Test Name: successfully update a user's information
# Except Output: user's name
print("test 7 -- test 4.1.1.4")
print("Test Name : successfully update a user's information with gender")
print("Except Output: user's name gender M")
print("Actual Output:")
id=1
user = User_info_model.db_get_one_user_by_id(id)
user.gender = "M"
new_user = User_info_model.db_update_one_user_info(user)
print(user.user_name)
print(user.gender)
