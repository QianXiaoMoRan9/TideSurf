from data_source.postprocessing.aicai_conversion import SinaCodePrefixAdder

if __name__ == "__main__":
    DATA_FOLDER = "/home/steven/Desktop/Fast500/sina-raw"
    CUR_DATE = "2020-12-22"
    adder = SinaCodePrefixAdder(DATA_FOLDER, CUR_DATE)

    record_1 = {
        "name": "平安银行"
    }
    code_1 = "000001"
    assert adder.convert_code(record_1, code_1) == "sz000001"

    record_2 = {
        "name": "太阳能"
    }
    code_2 = "000591"
    assert adder.convert_code(record_2, code_2) == "sz000591"

    record_3 = {
        "name": "太阳能"
    }
    code_3 = "993583"
    assert adder.convert_code(record_3, code_3) == "sh993583", "actual: {}".format(code_3)

    record_4 = {
        "name": "智慧农业"
    }
    code_4 = "000816"
    assert adder.convert_code(record_4, code_4) == "sz000816"

    record_5 = {
        "name": "上证公用"
    }
    code_5 = "000041"
    assert adder.convert_code(record_5, code_5) == "sh000041"

    record_6 = {
        "name": "细分医药"
    }
    code_6 = "000814"
    assert adder.convert_code(record_6, code_6) == "sh000814"

    record_7 = {
        "name": "万科Ａ"
    }
    code_7 = "000002"
    assert adder.convert_code(record_7, code_7) == "sz000002"

    record_7 = {
        "name": "Ａ股指数"
    }
    code_7 = "000002"
    assert adder.convert_code(record_7, code_7) == "sh000002"

