#include "tidesurf/runner.h"

using namespace tidesurf;

TideSurfConfig::TideSurfConfig(const char *config_json_file)
        : config_json_file_path_(config_json_file) {
    rapidjson::Document document;
    std::shared_ptr<std::string> json_string = read_file_to_string(config_json_file);
    char *cstring = new char[json_string->length() + 1];
    std::strcpy(cstring, json_string->c_str());

    int parse_result = document.ParseInsitu(cstring).HasParseError();

    ASSERT(!parse_result, "Failed to parse config json object");
    ASSERT(document.IsObject(), "Config json parse result should be json object");

    ASSERT(document.HasMember("history_folder_path"), "Config json missing attribute history_folder_path");
    ASSERT(document["history_folder_path"].IsString(), "history_folder_path should be valid string");
    ASSERT(document.HasMember("app_data_path"), "Config json missing attribute app_data_path");
    ASSERT(document["app_data_path"].IsString(), "app_data_path should be valid string");

    history_folder_path_ = document["history_folder_path"].GetString();
    app_data_path_ = document["app_data_path"].GetString();
    delete cstring;
}

Runner::Runner(const char *config_json_path) {
    InitConfiguration(config_json_path);
    InitStockMap(config_);
}

void Runner::InitConfiguration(const char *config_json_path) {
    config_ = *(new TideSurfConfig(config_json_path));
}

void Runner::InitStockMap(TideSurfConfig config) {
    stock_map_ = *(new std::unordered_map<std::string, Stock>());
    std::string stock_list_path = config_.app_data_path_ + "/stock_list.parquet";
    RecordTable stock_list_table = RecordTable(SINA_A_STOCK_LIST_PARQUET_TABLE_SCHEMA, stock_list_path);
    RecordTableStringColumnIterator code_iterator = RecordTableStringColumnIterator(stock_list_table, 0);
    RecordTableStringColumnIterator name_iterator = RecordTableStringColumnIterator(stock_list_table, 0);
    RecordTableStringColumnIterator abbrev_iterator = RecordTableStringColumnIterator(stock_list_table, 0);
    while (code_iterator.HasNext()) {
        std::string code = code_iterator.Next();
        stock_map_.emplace(code, Stock(code, name_iterator.Next()));
    }
}