import os
import robin-stocks as r

class TestLogin:
    @classmethod
    def setup_class(cls):
        print('setting up')
        r.login(os.environ['robin_username'], os.environ['robin_password'])
     
    @classmethod
    def teardown_class(cls):
        print('logging out')
        r.logout()
        
     def test_one():
        profile_info = r.load_account_profile()
        print(profile_info)
        assert profile_info
        
        
        
# # content of test_robin.py
# def func(x):
#     return x + 1

# def test_answer():
#     assert func(3) == 4

# #    assert os.environ['robin_username'] == "blah"
