#pragma once
#include "rapidjson/document.h"
#include "tidesurf/file_io.h"

namespace tidesurf
{
    class AppConfig
    {
    public:
        AppConfig(const char *config_path)
        {
            rapidjson::Document document;
            std::shared_ptr<std::string> json_string = read_file_to_string(config_path);
            document.Parse(json_string->c_str());
            history_data_folder_ = document["history_data_folder"].GetString();
            app_data_folder_ = document["app_data_folder"].GetString();
        }

    private:
        std::string history_data_folder_;
        std::string app_data_folder_;
    };
} // namespace tidesurf
