import logging 
import os
from logger.enums import MarketType
from datetime import datetime 

class Logger(object):
    MARKET_TYPE_SUBFOLDER_MAP = {
        MarketType.A_STOCK: "astock",
        MarketType.US_STOCK: "us_stock"
    }
    def __init__(self, app_folder, cur_date, market_type, module, print_verbose = True):
        assert os.path.exists(app_folder), "Logger Init Error: app_folder must exists, got: {}".format(app_folder)
        
        assert market_type in self.MARKET_TYPE_SUBFOLDER_MAP, "Logger Init Error: market_type provided does not exists, got: {}".format(market_type)
        logger_folder = os.path.join(app_folder, self.MARKET_TYPE_SUBFOLDER_MAP[market_type])
        if not os.path.exists(logger_folder):
            os.mkdir(logger_folder)
        
        now_dt = datetime.now()
        self._log_file = os.path.join(logger_folder, "{}_{}-{}-{}.json".format(cur_date, now_dt.hour, now_dt.minute, now_dt.second))
        logging.basicConfig(filename=self._log_file, filemode="a")
        
        self._print_verbose = print_verbose

        logging.info("================== Start logging module {} ======================".format(module))
        if print_verbose:
            print("================== Start logging module {} ======================".format(module))

    @property
    def log_file(self):
        return self._log_file

    @property
    def print_verbose(self):
        return self._print_verbose

    def info(self, msg):
        if self.print_verbose:
            print("[INFO] {}".format(msg))
        logging.info(msg)
    
    def warning(self, msg):
        if self.print_verbose:
            print("[WARNING] {}".format(msg))
        logging.warning(msg)

    def error(self, msg):
        if self.print_verbose:
            print("[ERROR] {}".format(msg))
        logging.error(msg)


    