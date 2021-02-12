import logging
import os 
from datetime import datetime
from logger.enums import MarketType

class Logger(object):
    MARKET_SUB_FOLDER_NAME_DICT = {
        MarketType.A_STOCK: "astock",
        MarketType.US_STOCK: "us_stock"
    }
    def __init__(self, app_folder, cur_date, market_type, module):
        assert os.path.exists(app_folder), "Logger construction error: app_folder must have existed"
        assert market_type in self.MARKET_SUB_FOLDER_NAME_DICT, "Logger construction error: provided market type not implemented: {}".format(market_type)
        
        log_subfolder = os.path.join(app_folder, self.MARKET_SUB_FOLDER_NAME_DICT[market_type])
        if not os.path.exists(log_subfolder):
            os.mkdir(log_subfolder) 
        cur_datetime = datetime.now()

        self._log_path = os.path.join(log_subfolder, "{}_{}-{}-{}.log".format(
                cur_date,
                cur_datetime.hour ,
                cur_datetime.minute,
                cur_datetime.second
            )
        )

        logging.basicConfig(fllename=self._log_path)
        logging.info("================ Start Logging for Module {} =======================".format(module))
    
    @property 
    def log_path(self):
        return self._log_path

    def info(self, msg):
        logging.info(msg)
    
    def warning(self, msg):
        logging.warning(msg)
    
    def error(self, msg):
        logging.error(msg)
    
    
