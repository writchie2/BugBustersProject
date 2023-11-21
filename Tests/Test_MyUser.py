import unittest
from SchedulingApp.models import MyUser


#Testing constructor
class TestInit(unittest.TestCase):
    
    def setUp(self):
        good_email = "default@uwm.edu"
        good_pass = "PassWord!123"
        good_first = "First"
        good_last = "Last"
        good_num = "(123)456-7890"
        good_add = "1234 Main St"
        good_city = "Milwaukee"
        good_state = "WI"
        good_zip = 53206
        good_role = "ad"

        bad_email7 = MyUser("")
        bad_email7 = MyUser(" ")
        bad_email7 = MyUser("b")
        bad_email3 = MyUser("bad ")
        bad_email1 = MyUser("bademail.com")
        bad_email2 = MyUser("bademail@")
        bad_email4 = MyUser("b ad@uwm.edu")
        bad_email5 = MyUser(" bad@uwm.edu")
        bad_email6 = MyUser("bad@uwm.edu ")


        bad_password1 = MyUser(good_email, "")
        bad_password2 = MyUser(good_email, " ")
        bad_password3 = MyUser(good_email, "a")
        bad_password4 = MyUser(good_email, " a")
        bad_password5 = MyUser(good_email, "a ")
        bad_password6 = MyUser(good_email, "password")
        bad_password7 = MyUser(good_email, "Password")
        bad_password8 = MyUser(good_email, "Password!")

        bad_name1 = ""
        bad_name2 = " "
        bad_name3 = "P"
        bad_name4 = "1234"
        bad_name5 = "P3rson"
        bad_name6 = " Person"
        bad_name7 = "Person "


        a = MyUser()
        a_email = a.email
        a_password = a.password
        a_first_name = a.firstName
        a_last_name = a.lastName
        a_num = a.phoneNumber
        a_add = a.streetAddress
        a_st = a.streetAddress
        a_city = a.city
        a_state = a.state
        a_zip = a.zipcode
        a_role = a.role


    def test_no_at(self):
        pass
        
    def test_no_args(self):

        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
