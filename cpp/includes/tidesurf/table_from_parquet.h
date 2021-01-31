#pragma once
#include <arrow/api.h>
#include <arrow/io/api.h>
#include <parquet/arrow/reader.h>
#include <parquet/arrow/writer.h>
#include <parquet/exception.h>
#include <vector>

#include "tidesurf_macros.h"
#include "tidesurf_types.h"

using arrow::DoubleBuilder;
using arrow::Int64Builder;
using arrow::ListBuilder;

namespace tidesurf
{

    class TableFromParquet
    {

    public:
        TableFromParquet(ParquetTableSchemaVector schema_vector, const std::string &table_file_path)
        {
            schema_ptr_ = std::make_shared<arrow::Schema>(*(new ParquetTableSchemaVector(schema_vector)));
            LoadParquetToTable(table_file_path);
            ASSERT(schema_ptr_->Equals(*table_ptr_->schema()), "Table schema does not match");
        }

        void LoadParquetToTable(const std::string &table_file_path)
        {
            std::shared_ptr<arrow::io::ReadableFile> infile;
            PARQUET_ASSIGN_OR_THROW(
                infile,
                arrow::io::ReadableFile::Open(table_file_path,
                                              arrow::default_memory_pool()));

            std::unique_ptr<parquet::arrow::FileReader> reader;
            PARQUET_THROW_NOT_OK(
                parquet::arrow::OpenFile(infile, arrow::default_memory_pool(), &reader));
            PARQUET_THROW_NOT_OK(reader->ReadTable(&table_ptr_));
        }

        std::shared_ptr<arrow::Table> GetTable() {
            return table_ptr_;
        }

        std::shared_ptr<arrow::Schema> GetSchema() {
            return schema_ptr_;
        }

        std::string GetStringEntry(int64_t row, int64_t column) {
            return this->GetColumn<arrow::StringArray>(column)->GetString(row);
        }

        template <class ArrayType>
        std::shared_ptr<ArrayType> GetColumn(int column) {
            return std::static_pointer_cast<ArrayType>(table_ptr_->column(column)->chunk(0));
        }

        int64_t NumRows() {
            return table_ptr_->num_rows();
        }

        int64_t NumColumn() {
            return schema_ptr_->fields().size();
        }

    private:
        std::shared_ptr<arrow::Schema> schema_ptr_;
        std::shared_ptr<arrow::Table> table_ptr_;
    };

} // namespace tidesurf
