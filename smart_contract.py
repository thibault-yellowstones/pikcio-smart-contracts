
def contract_test():

    data = 3

    def test():
        global data
        data += 3
        return data


@accepts()
class contract_test2(object):
    data = 3

    @staticmethod
    def test():
        contract_test2.self.data += 3
        return data
