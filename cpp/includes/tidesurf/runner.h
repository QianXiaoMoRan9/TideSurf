#include <cstdint>
#include <iostream>
#include <unordered_map>
#pragma once
#include <pthread.h>

#include "rapidjson/document.h"

#include "tidesurf/tidesurf_macros.h"
#include "tidesurf/globals.h"
#include "tidesurf/table_from_parquet.h"
#include "tidesurf/stock.h"

namespace tidesurf
{

    /**
     * @brief The arch driver class for the program
     * 
     * Responsible for initializing:
     * The data receiver
     * Load the previous history data
     * Load configurations
     * Start the server for web client
     * 
     */
    class Runner
    {
    public:
        Runner(const char *config_json_path)
        {
        }

        void InitConfiguration();

        void InitDatReceiver();

        void InitStockMap()
        {
        }

        void InitHistoryData();

        void InitWebServer();

    private:
        std::unordered_map<std::string, Stock> stock_map_;
    };

    class TideSurfConfig
    {
    public:
        
        std::string config_json_file_path_; // The config file path passed from execution arg
        std::string history_folder_path_; // The root folder that stores the stock data and stock list
        std::string app_data_path_; // Data generated by the app

        TideSurfConfig(const char *config_json_file)
            : config_json_file_path_(config_json_file)
        {
            LoadJsonConfig();
        }

        void LoadJsonConfig() {
            Document document;
            
        }
    };

} // namespace tidesurf
