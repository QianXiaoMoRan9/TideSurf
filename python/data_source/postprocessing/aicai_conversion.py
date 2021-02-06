"""
Sina code without prefix to distinct code conversion:

first process the stock_list into:
(code, name) pairs:
- name eliminate the '.', for example 太阳能.指数基金 -> 太阳能
- name convert to sina version
- code add prefix if non. 
"""

import json 
from data_source.stock.easy_quotation_sina_real import add_stock_prefix, get_stock_type

class SinaCodePrefixAdder(object):
    STOCK_NAME_DIFF_DICT = {
        '星徽精密': "星徽股份",
        "启迪古汉": "启迪药业",
        "B股指数": "Ｂ股指数",
        "50AH优选": "50AH优选",
        "A股资源": "A股资源",
        "\u94f6\u884cA": "\u94f6\u884cA",
        "\u5e26\u8defA": "\u5e26\u8defA",
        "\u5f18\u76c8A": "\u5f18\u76c8A",
        "\u767d\u4e91\u5c71A": "\u767d\u4e91\u5c71A",
        "\u53cc\u503aA": "\u53cc\u503aA",
        "\u76c8\u534eA": "\u76c8\u534eA",
        "1000A": "1000A",
        "NCF\u73af\u4fddA": "NCF\u73af\u4fddA",
        "\u4f53\u80b2A": "\u4f53\u80b2A",
        "\u4e2d\u8bc190A": "\u4e2d\u8bc190A",
        "\u94f6\u884c\u80a1A": "\u94f6\u884c\u80a1A",
        "\u6709\u8272800A": "\u6709\u8272800A",
        "\u5de5\u4e1a4A": "\u5de5\u4e1a4A",
        "\u4fe1\u606f\u5b89A": "\u4fe1\u606f\u5b89A",
        "\u5730\u4ea7A\u7aef": "\u5730\u4ea7A\u7aef",
        "\u5b89\u9053\u9ea6A": "\u5b89\u9053\u9ea6A",
        "MSCICHNA": "MSCICHNA",
        "\u4e92\u8054A\u7ea7": "\u4e92\u8054A\u7ea7",
        "\u6539\u9769A": "\u6539\u9769A",
        "*ST\u77f3\u5316A": "*ST\u77f3\u5316A",
        "\u56fd\u4f01\u6539A": "\u56fd\u4f01\u6539A",
        "\u6caa\u6df1300A": "\u6caa\u6df1300A",
        "\u4e2d\u822a\u519bA": "\u4e2d\u822a\u519bA",
        "MSCIA\u80a1": "MSCIA\u80a1",
        "\u4e2d\u5173\u6751A": "\u4e2d\u5173\u6751A",
        "\u4f20\u5a92A\u7ea7": "\u4f20\u5a92A\u7ea7",
        "\u8d44\u6e90A": "\u8d44\u6e90A",
        "\u8bc1\u5238A\u57fa": "\u8bc1\u5238A\u57fa",
        "\u9ad8\u94c1A\u7ea7": "\u9ad8\u94c1A\u7ea7",
        "\u8bc1\u5238\u80a1A": "\u8bc1\u5238\u80a1A",
        "\u5609\u5b9e300A": "\u5609\u5b9e300A",
        "AI\u667a\u80fd": "AI\u667a\u80fd",
        "\u4e2d\u8bc1500A": "\u4e2d\u8bc1500A",
        "\u7f51\u91d1A": "\u7f51\u91d1A",
        "\u4e0a50A": "\u4e0a50A",
        "\u6cf0\u4fe1400A": "\u6cf0\u4fe1400A",
        "\u4e0a\u8bc150A": "\u4e0a\u8bc150A",
        "\u751f\u7269A": "\u751f\u7269A",
        "\u4e00\u5e26\u4e00A": "\u4e00\u5e26\u4e00A",
        "\u521b\u4e1a\u677fA": "\u521b\u4e1a\u677fA",
        "\u91d1\u878d\u5730A": "\u91d1\u878d\u5730A",
        "AIETF": "AIETF",
        "\u6df1\u5357\u7535A": "\u6df1\u5357\u7535A",
        "\u9ad8\u94c1A": "\u9ad8\u94c1A",
        "\u5efa\u4fe150A": "\u5efa\u4fe150A",
        "\u767d\u9152A": "\u767d\u9152A",
        "\u65b0\u80fd\u6e90A": "\u65b0\u80fd\u6e90A",
        "\u521b\u4e1a\u80a1A": "\u521b\u4e1a\u80a1A",
        "\u519b\u5de5A": "\u519b\u5de5A",
        "\u6709\u8272A": "\u6709\u8272A",
        "\u94a2\u94c1A": "\u94a2\u94c1A",
        "\u9152A": "\u9152A",
        "\u8bc1\u4fddA": "\u8bc1\u4fddA",
        "\u521b\u4e1aA": "\u521b\u4e1aA",
        "\u5609\u5b9e50A": "\u5609\u5b9e50A",
        "\u4e92\u8054\u7f51A": "\u4e92\u8054\u7f51A",
        "\u667a\u80fdA": "\u667a\u80fdA",
        "\u5927\u4e1c\u6d77A": "\u5927\u4e1c\u6d77A",
        "\u98df\u54c1A": "\u98df\u54c1A",
        "\u56fd\u8bc1A50": "\u56fd\u8bc1A50",
        "\u5408\u6da6A": "\u5408\u6da6A",
        "\u521b\u4e1a\u677fPA": "\u521b\u4e1a\u677fPA",
        "\u4fdd\u9669A": "\u4fdd\u9669A",
        "\u6df1\u7269\u4e1aA": "\u6df1\u7269\u4e1aA",
        "50AH": "50AH",
        "\u533b\u7597A": "\u533b\u7597A",
        "A50ETF": "A50ETF",
        "\u8bc1\u5238A\u7ea7": "\u8bc1\u5238A\u7ea7",
        "\u94f6\u884cA\u7aef": "\u94f6\u884cA\u7aef",
        "\u6052\u751fA": "\u6052\u751fA",
        "\u533b\u836fA": "\u533b\u836fA",
        "\u65b0\u80fd\u8f66A": "\u65b0\u80fd\u8f66A",
        "PT\u91d1\u7530A": "PT\u91d1\u7530A",
        "\u7164\u70adA": "\u7164\u70adA",
        "\u743c\u6c11\u6e90A": "\u743c\u6c11\u6e90A",
        "\u795e\u57ceA\u9000": "\u795e\u57ceA\u9000",
        "TMT\u4e2d\u8bc1A": "TMT\u4e2d\u8bc1A",
        "\u4e2d\u8bc1100A": "\u4e2d\u8bc1100A",
        "\u4fe1\u606fA": "\u4fe1\u606fA",
        "MSCIAETF": "MSCIAETF",
        "\u4f20\u5a92A": "\u4f20\u5a92A",
        "\u5238\u5546A\u7ea7": "\u5238\u5546A\u7ea7",
        "TMTA": "TMTA",
        "\u6df1A\u533b\u836f": "\u6df1A\u533b\u836f",
        "\u8bc1\u5238A": "\u8bc1\u5238A",
        "\u5238\u5546A": "\u5238\u5546A",
        "\u751f\u7269\u836fA": "\u751f\u7269\u836fA",
        "SW\u533b\u836fA": "SW\u533b\u836fA",
        "\u5bcc\u65f6A50": "\u5bcc\u65f6A50",
        "\u7164\u70adA\u57fa": "\u7164\u70adA\u57fa",
        "\u7a33\u5065\u503aA": "\u7a33\u5065\u503aA",
        "\u6df1\u6210\u6307A": "\u6df1\u6210\u6307A",
        "\u5065\u5eb7A": "\u5065\u5eb7A",
        "A\u80a1\u8d44\u6e90": "A\u80a1\u8d44\u6e90",
        "\u5730\u4ea7A": "\u5730\u4ea7A",
        "\u91cd\u7ec4A": "\u91cd\u7ec4A",
        "*ST\u4e2d\u534eA": "*ST\u4e2d\u534eA",
        "\u6052\u4e2d\u4f01A": "\u6052\u4e2d\u4f01A",
        "\u94f6\u534e300A": "\u94f6\u534e300A",
        "\u73af\u4fddA\u7ea7": "\u73af\u4fddA\u7ea7",
        "\u519b\u5de5A\u7ea7": "\u519b\u5de5A\u7ea7",
        "\u533b\u836f800A": "\u533b\u836f800A",
        "\u519b\u5de5\u80a1A": "\u519b\u5de5\u80a1A",
        "\u623f\u5730\u4ea7A": "\u623f\u5730\u4ea7A",
        "\u91d1\u878dA": "\u91d1\u878dA",
        "\u7164\u70adA\u7ea7": "\u7164\u70adA\u7ea7",
        "\u4e92\u8054A": "\u4e92\u8054A",
        "\u56fd\u9632A": "\u56fd\u9632A",
        "PT\u4e2d\u6d69A": "PT\u4e2d\u6d69A",
        "50AH\u4f18\u9009": "50AH\u4f18\u9009"
    }

    PREFIX_SET = {
        "sh",
        "sz",
        "of",
        "zz"
    }
        
    def __init__(self, data_folder, cur_date):
        self.data_folder = data_folder
        self.cur_date = cur_date

        "{(sz000591, 太阳能), (sh600405, 股票名)}"
        self.aicai_pair_set = set()
        "(000591, 太阳能) -> (sz000591, 太阳能)"
        self.sina_pair_to_aicai_pair_dict = dict()

        self.load_aicai_stock_list()

    def load_aicai_stock_list(self):
        with open(self.get_stock_list_path(), "r") as json_f:
            stock_list = json.load(json_f)["stocks"]
            for stock in stock_list:
                self.aicai_pair_set.add(
                    (add_stock_prefix(stock[0]), self.convert_aicai_name_to_sina_name(stock[1]))
                )

    def convert_aicai_name_to_sina_name(self, string):
        string = string.split('.')[0]

        if (string in SinaCodePrefixAdder.STOCK_NAME_DIFF_DICT):
            return SinaCodePrefixAdder.STOCK_NAME_DIFF_DICT[string]
        
        return string.replace("A", "Ａ")

    def convert_code(self, record, original_code):
        code = original_code
        if original_code.startswith(('60', '30', '00')):
            found = False
            # if new stock starts with N or C: C全福, N泰山
            if (record["name"].startswith(('N', 'C')) and ord(record["name"][1]) > 127):
                code = add_stock_prefix(original_code)
                found = True
            else:
                sina_pair = (original_code, record["name"])
                if sina_pair in self.sina_pair_to_aicai_pair_dict:
                    code = self.sina_pair_to_aicai_pair_dict[sina_pair][0]
                    found = True
                else:
                    if sina_pair in self.aicai_pair_set:
                        code = original_code
                        self.sina_pair_to_aicai_pair_dict[sina_pair] = sina_pair
                        found = True
                    else:
                        for prefix in SinaCodePrefixAdder.PREFIX_SET:
                            new_code = prefix + original_code
                            new_pair = (new_code, record["name"])
                            if (new_pair in self.aicai_pair_set):
                                code = new_code
                                self.sina_pair_to_aicai_pair_dict[sina_pair] = new_pair
                                found = True
                                break
            assert found, "Must have found one from aicai {}, {}".format(original_code, record["name"])
        else:
            code = add_stock_prefix(original_code)
        return code
    def get_stock_list_path(self):
        return "{}/{}/data/stock_list_{}.json".format(self.data_folder, self.cur_date, self.cur_date)

