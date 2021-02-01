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

    class RecordTable
    {

    public:
        RecordTable(ParquetTableSchemaVector schema_vector, const std::string &table_file_path)
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

        std::shared_ptr<arrow::Table> GetTable()
        {
            return table_ptr_;
        }

        std::shared_ptr<arrow::Schema> GetSchema()
        {
            return schema_ptr_;
        }

        // std::string GetStringEntry(int64_t row, int64_t column) {
        //     return this->GetColumn<arrow::StringArray>(column)->GetString(row);
        // }

        std::shared_ptr<arrow::ChunkedArray> GetColumnChunkArray(int column)
        {
            return table_ptr_->column(column);
        }

        int64_t NumRows()
        {
            return table_ptr_->num_rows();
        }

        int64_t NumColumn()
        {
            return schema_ptr_->fields().size();
        }

    private:
        std::shared_ptr<arrow::Schema> schema_ptr_;
        std::shared_ptr<arrow::Table> table_ptr_;
    };

    template <class ColumnArrayType, class ColumnDataType>
    class RecordTableColumnIterator
    {
    public:
        RecordTableColumnIterator(RecordTable table, int64_t column)
            : column_index_(column)
        {
            column_ptr_ = table.GetColumnChunkArray(column_index_);
            num_chunks_ = column_ptr_->num_chunks();
            chunk_size_vector_ = std::vector<int64_t>();
            for (int64_t i = 0; i < num_chunks_; i++)
            {
                chunk_size_vector_.push_back(column_ptr_->chunk(i)->length());
            }
            ResetToStart();

            if (HasNext()) {
                chunk_ptr_ = GetChunk(cur_chunk_);
            }
        }

        /**
         * @brief Given an row number from the outside, break it down into chunk index + chunk row index
         * 
         * @param row_number 
         * @return std::pair<int64_t, int64_t> 
         */
        std::pair<int64_t, int64_t> GetChunkAndIndex(int64_t row_number) const {
            int64_t total_size = 0;
            int chunk_index = 0;
            while (total_size <= row_number && chunk_index < chunk_size_vector_.size()) {
                total_size += chunk_size_vector_[chunk_index];
                chunk_index ++;
            }
            if (total_size <= row_number && chunk_index >= chunk_size_vector_.size()) {
                ASSERT(false, "Row number of GetChunkAndIndex out of bound");
            }

            int64_t new_row_index = row_number - (total_size - chunk_size_vector_[chunk_index]);
            return std::make_pair<int64_t, int64_t>(chunk_index, new_row_index);
        }

        void ResetToStart() {
            cur_chunk_ = 0;
            cur_chunk_row_ = 0
        }

        void Advance() {
            if (cur_chunk_row_ == chunk_size_vector_[cur_chunk_]) {
                cur_chunk_ ++;
                cur_chunk_row_ = 0;
                if (cur_chunk < num_chunks_) {
                    chunk_ptr_ = GetChunk(cur_chunk_);
                } else {
                    chunk_ptr_ = nullptr;
                }
            } else {
                cur_chunk_row_ ++;
            }
        }

        bool HasNext() {
            if (cur_chunk_ >= num_chunks_) {
                return false;
            }
            if (cur_chunk_ == num_chunks_ - 1 && cur_chunk_row_ == chunk_size_vector_[cur_chunk_]) {
                return false;
            }
            return true;
        }

        std::shared_ptr<ColumnArrayType> GetChunk(int64_t chunk_index) {
            return std::static_pointer_cast<ColumnArrayType>(column_ptr_->chunk(chunk_index));
        }

    protected:
        std::shared_ptr<arrow::ChunkedArray> column_ptr_;
        std::shared_ptr<ColumnArrayType> chunk_ptr_;
        int64_t column_index_;
        int64_t num_row_;
        int64_t cur_chunk_;
        int64_t cur_chunk_row_;
        int64_t num_chunks_;
        std::vector<int64_t> chunk_size_vector_;
        
    };

    class RecordTableStringColumnIterator : RecordTableColumnIterator<arrow::StringArray, std::string>
    {
    public:
        RecordTableStringColumnIterator(RecordTable table, int64_t column)
            : RecordTableColumnIterator(table, column)
        {
        }

        std::string Next() {
            DEBUG_ASSERT(HasNext(), "RecordTableIterator should call HasNext to check before calling Next()");
            std::string entry = chunk_ptr_->GetString(cur_chunk_row_);
            Advance();
            return entry;
        }
    };

    template <class ColumnArrayType, class ColumnDataType>
    class RecordTableValueColumnIterator : RecordTableColumnIterator<ColumnArrayType, ColumnDataType>
    {
    public:
        RecordTableValueColumnIterator(RecordTable table, int64_t column)
            : RecordTableColumnIterator(table, column)
        {
        }

        ColumnDataType Next() {
            DEBUG_ASSERT(HasNext(), "RecordTableIterator should call HasNext to check before calling Next()");
            ColumnDataType entry = chunk_ptr_->Value(cur_chunk_row_);
            Advance();
            return entry;
        }
    };

    class RecordTableInt64ColumnIterator : RecordTableValueColumnIterator<arrow::Int64Array, int64_t>
    {
    public:
        RecordTableInt64ColumnIterator(RecordTable table, int64_t column)
            : RecordTableValueColumnIterator(table, column)
        {
        }
    };

    class RecordTableDoubleColumnIterator : RecordTableValueColumnIterator<arrow::DoubleArray, double>
    {
    public:
        RecordTableDoubleColumnIterator(RecordTable table, int64_t column)
            : RecordTableValueColumnIterator(table, column)
        {
        }
    };

} // namespace tidesurf
