class TestCase(object):

    def setUp(self):
        pass 

    def tearDown(self):
        pass 


    def run_test_cases(self):
        raise NotImplementedError("Must register test cases")


    def run(self):
        self.setUp()
        self.run_test_cases()
        self.tearDown()

    def assertEqual(self, expect, actual):
        if not expect == actual:
            print("Expect Equal: expect: {}, actual {}".format(expect, actual))
            self.tearDown()
            assert False
    
    def assertAlmostEqual(self, expect, actual, thresh = 1e-5):
        if not abs(expect - actual) < thresh:
            print("Expect Almost Equal: expect: {}, actual {}".format(expect, actual))
            self.tearDown()
            assert False
    
    def assertNotEqual(self, expect, actual):
        if expect == actual:
            print("Expect NOT Equal: expect: {}, actual {}".format(expect, actual))
            self.tearDown()
            assert False
    
    def assertFalse(self, expression):
        if expression:
            print("Expect False")
            self.tearDown()
            assert False
    
    def assertTrue(self, expression):
        if not expression:
            print("Expect True")
            self.tearDown()
            assert False