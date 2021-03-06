import os 

class Postprocessor(object):
    
    def __init__(self, source_data_folder, app_data_folder):
        self._source_data_folder = source_data_folder
        self._app_data_folder = app_data_folder

        self._app_astock_folder = os.path.join(self.app_data_folder, "astock")
        self._app_astock_record_data_folder = os.path.join(self.app_astock_folder, "record_data")
        self._app_astock_record_data_realtime_folder = os.path.join(self.app_astock_record_data_folder, "realtime_data")
        self.verify_folder_structure()
    
    def verify_folder_structure(self):
        assert os.path.exists(self.source_data_folder)
        assert os.path.exists(self.app_data_folder)
        # setup folders in the app_data_folder
        astock_folder = self.app_astock_folder
        if not os.path.exists(self.app_astock_folder):
            os.mkdir(astock_folder)
        
        log_folder = self.app_astock_log_folder
        if not os.path.exists(log_folder):
            os.mkdir(log_folder)
        
        temp_folder = self.app_astock_temp_folder
        if not os.path.exists(temp_folder):
            os.mkdir(temp_folder)
        
        stock_selection_folder = self.app_astock_stock_selection_folder
        if not os.path.exists(stock_selection_folder):
            os.mkdir(stock_selection_folder)
        
        record_data_folder = self.app_astock_record_data_folder
        if not os.path.exists(record_data_folder):
            os.mkdir(record_data_folder)

        realtime_folder = self.app_astock_record_data_realtime_folder
        if not os.path.exists(realtime_folder):
            os.mkdir(realtime_folder)

        daily_breakdown_folder = self.app_astock_record_data_daily_breakdown_folder
        if not os.path.exists(daily_breakdown_folder):
            os.mkdir(daily_breakdown_folder)
        
    def get_app_astock_record_data_realtime_date_folder(self, data_date):
        return os.path.join(self.app_astock_record_data_realtime_folder, data_date)
    
    def get_app_astock_record_data_realtime_date_partition(self, data_date, partition):
        assert type(partition) == int
        return os.path.join(
            self.get_app_astock_record_data_realtime_date_folder(data_date),
            "{}.parquet".format(partition)
        )
    
    def get_app_astock_record_data_realtime_date_code_to_partition_map(self, data_date):
        return os.path.join(
            self.get_app_astock_record_data_realtime_date_folder(data_date),
            "code_to_partition_map.json"
        )
    
    def get_app_astock_data_realtime_date_latest_adjust_record(self, data_date):
        return os.path.join(
            self.get_app_astock_record_data_realtime_date_folder(data_date),
            "latest_adjust_record.json"
        )

    def get_app_astock_data_daily_breakdown_date_folder(self, data_date):
        return os.path.join(self.app_astock_record_data_daily_breakdown_folder, data_date)
    
    def get_app_astock_data_daily_breakdown_date_price_breakdown(self, data_date):
        return os.path.join(
            self.get_app_astock_data_daily_breakdown_date_folder(data_date),
            "price_breakdown.parquet"
        )

    def get_source_date_folder(self, data_date):
        return os.path.join(
            self.source_data_folder,
            data_date
        )

    def get_source_date_partition(self, data_date, partition):
        assert type(partition) == int
        
        return os.path.join(
            self.get_source_date_folder(data_date),
            "{}.parquet".format(partition)
        )
    
    def get_source_date_stock_list(self, data_date):
        return os.path.join(
            self.get_source_date_folder(data_date),
            "stock_list.parquet"
        )
    
    def get_source_date_split_adjust(self, data_date):
        return os.path.join(
            self.get_source_date_folder(data_date),
            "split_adjust.parquet"
        )
    
    def get_source_date_code_to_partition_map(self, data_date):
        return os.path.join(
            self.get_source_date_folder(data_date),
            "code_to_partition_map.json"
        )


    @property
    def source_data_folder(self):
        return self._source_data_folder

    @property
    def app_data_folder(self):
        return self._app_data_folder

    @property
    def app_astock_folder(self):
        return self._app_astock_folder
    
    @property 
    def app_astock_log_folder(self):
        return os.path.join(self.app_astock_folder, "log")
    
    @property
    def app_astock_temp_folder(self):
        return os.path.join(self.app_astock_folder, "temp")
    
    @property 
    def app_astock_stock_selection_folder(self):
        return os.path.join(self.app_astock_folder, "stock_selection")
    
    @property
    def app_astock_record_data_folder(self):
        return self._app_astock_record_data_folder
    
    @property
    def app_astock_record_data_realtime_folder(self):
        return self._app_astock_record_data_realtime_folder

    @property
    def app_astock_record_data_daily_breakdown_folder(self):
        return os.path.join(self.app_astock_record_data_folder, "daily_breakdown")
    
