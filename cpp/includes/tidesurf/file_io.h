#include <fstream>
#include <memory>
#include <iostream>
#include "tidesurf/tidesurf_macros.h"

namespace tidesurf {
    
    std::shared_ptr<std::string> read_file_to_string(const char *file_path) {
        std::ifstream in_file(file_path);
        std::string content( (std::istreambuf_iterator<char>(in_file) ),
                            (std::istreambuf_iterator<char>()    ) );

        return std::make_shared<std::string>(content);
    }

    void write_string_to_file(const char *file_path, std::string str, std::ios_base::openmode mode) {
        std::ofstream out_file;
        out_file.open(file_path, mode);
        out_file << str;
        out_file.close();
    }

    void write_bytes_to_file(const char *file_path, const char *bytes, size_t size, std::ios_base::openmode mode) {
        std::ofstream out_file;
        out_file.open(file_path, mode);
        out_file.write(bytes, size);
        out_file.close();
    }

    void write_string_to_file_append(const char *file_path, std::string str) {
        write_string_to_file(file_path, str, std::ofstream::app | std::ofstream::out);
    }

    void write_string_to_file_overwrite(const char *file_path, std::string str) {
        write_string_to_file(file_path, str, std::ofstream::out);
    }

    void write_binary_to_file_append(const char *file_path, const char *bytes, size_t size) {
        write_bytes_to_file(file_path, bytes, size, std::ofstream::app | std::ofstream::out | std::ofstream::binary);
    }

    void write_binary_to_file_overwrite(const char *file_path, const char *bytes, size_t size) {
        write_bytes_to_file(file_path, bytes, size,  std::ofstream::out | std::ofstream::binary);
    }

    
}