import unittest

import tests.login_test as login_test
import tests.aes_gcm_test as aes_gcm_test
import tests.connect_db_1_test as connect_db_1_test
import tests.connect_db_2_test as connect_db_2_test
import tests.sql_validation_test as sql_validation_test


if __name__ == "__main__":
    suite = unittest.TestSuite()

    # login_test
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(login_test.Validater_Test))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(login_test.Hash_Test))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(login_test.Login_DB_Test))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(login_test.Login_Test))

    # connect_db_1_test
    #suite.addTests(unittest.TestLoader().loadTestsFromTestCase(connect_db_1_test.Validater_Test))
    #suite.addTests(unittest.TestLoader().loadTestsFromTestCase(connect_db_1_test.Hash_Test))
    #suite.addTests(unittest.TestLoader().loadTestsFromTestCase(connect_db_1_test.Conn_DB_DB_Test))
    #suite.addTests(unittest.TestLoader().loadTestsFromTestCase(connect_db_1_test.Test_Conn_Test))
    #suite.addTests(unittest.TestLoader().loadTestsFromTestCase(connect_db_1_test.Conn_DB_Test))

    # connect_db_2_test
    #suite.addTests(unittest.TestLoader().loadTestsFromTestCase(connect_db_2_test.DB_Connection_Test))
    #suite.addTests(unittest.TestLoader().loadTestsFromTestCase(connect_db_2_test.Conn_DB_2_Test))
    #suite.addTests(unittest.TestLoader().loadTestsFromTestCase(connect_db_2_test.Match_Role_Test))
    #suite.addTests(unittest.TestLoader().loadTestsFromTestCase(connect_db_2_test.Remove_User_Test))
    #suite.addTests(unittest.TestLoader().loadTestsFromTestCase(connect_db_2_test.Add_Users_Test))

    # aes_gcm_test
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(aes_gcm_test.AES_Test))

    # sql_validation_test
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(sql_validation_test.SQL_Validation_Test))


    unittest.TextTestRunner().run(suite)
