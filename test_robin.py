import os
import robin_stocks as r

class TestStocks:
    def test_quotes(self):
        profile_info = r.get_quotes('spy')
        print(profile_info)
        assert profile_info
        
    def test_name_apple(self):
        name = r.get_name_by_symbol('aapl')
        assert name == "Apple"

        
# class TestLogin:
#     @classmethod
#     def setup_class(cls):
#         print('setting up')
#         r.login(os.environ['robin_username'], os.environ['robin_password'])
     
#     @classmethod
#     def teardown_class(cls):
#         print('logging out')
#         r.logout()
        
#     def test_one(self):
#         profile_info = r.load_account_profile()
#         print(profile_info)
#         assert profile_info
