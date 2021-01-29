#include <cstdint>
#include <iostream>
#include <unordered_map>
#include <pthread.h>

#include "stock.h"

namespace tidesurf {

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
class Runner {
public:
Runner();

void InitConfiguration();

void InitDatReceiver();

void InitStockMap();

void InitHistoryData();

void InitWebServer();

private:
    std::unordered_map<std::string, Stock> stock_map_;
};

}
