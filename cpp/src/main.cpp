// Licensed to the Apache Software Foundation (ASF) under one
// or more contributor license agreements. See the NOTICE file
// distributed with this work for additional information
// regarding copyright ownership. The ASF licenses this file
// to you under the Apache License, Version 2.0 (the
// "License"); you may not use this file except in compliance
// with the License. You may obtain a copy of the License at
//
// http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing,
// software distributed under the License is distributed on an
// "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
// KIND, either express or implied. See the License for the
// specific language governing permissions and limitations
// under the License.

#include <iostream>
#include <arrow/api.h>
#include <arrow/io/api.h>
#include <parquet/arrow/reader.h>
#include <parquet/arrow/writer.h>
#include <parquet/exception.h>
#include <vector>

#include "tidesurf/server.h"
#include "tidesurf/record_table.h"
#include "tidesurf/globals.h"
#include "tidesurf/file_io.h"

using arrow::DoubleBuilder;
using arrow::Int64Builder;
using arrow::ListBuilder;

// #0 Build dummy data to pass around
// To have some input data, we first create an Arrow Table that holds
// some data.
std::shared_ptr<arrow::Table> generate_table() {
  arrow::Int64Builder i64builder;
  PARQUET_THROW_NOT_OK(i64builder.AppendValues({1, 2, 3, 4, 5}));
  std::shared_ptr<arrow::Array> i64array;
  PARQUET_THROW_NOT_OK(i64builder.Finish(&i64array));

  arrow::StringBuilder strbuilder;
  PARQUET_THROW_NOT_OK(strbuilder.Append("some"));
  PARQUET_THROW_NOT_OK(strbuilder.Append("string"));
  PARQUET_THROW_NOT_OK(strbuilder.Append("content"));
  PARQUET_THROW_NOT_OK(strbuilder.Append("in"));
  PARQUET_THROW_NOT_OK(strbuilder.Append("rows"));
  std::shared_ptr<arrow::Array> strarray;
  PARQUET_THROW_NOT_OK(strbuilder.Finish(&strarray));

  std::shared_ptr<arrow::Schema> schema = arrow::schema(
      {arrow::field("int", arrow::int64()), arrow::field("str", arrow::utf8())});

  return arrow::Table::Make(schema, {i64array, strarray});
}

// #1 Write out the data as a Parquet file
void write_parquet_file(const arrow::Table& table) {
  std::shared_ptr<arrow::io::FileOutputStream> outfile;
  PARQUET_ASSIGN_OR_THROW(
      outfile,
      arrow::io::FileOutputStream::Open("parquet-arrow-example.parquet"));
  // The last argument to the function call is the size of the RowGroup in
  // the parquet file. Normally you would choose this to be rather large but
  // for the example, we use a small value to have multiple RowGroups.
  PARQUET_THROW_NOT_OK(
      parquet::arrow::WriteTable(table, arrow::default_memory_pool(), outfile, 3));
}

// #2: Fully read in the file
arrow::Status read_whole_file() {
  std::cout << "Reading parquet-arrow-example.parquet at once" << std::endl;
  tidesurf::RecordTable *record_table = new tidesurf::RecordTable(tidesurf::STOCK_LIST_PARQUET_TABLE_SCHEMA, "/home/steven/Desktop/Fast500/astock_parquet/stock_list.parquet");
  std::shared_ptr<arrow::Table> table = record_table->GetTable();

//   auto turnovers = record_table->GetColumn<arrow::Int64Array>(30);

//   for (int64_t i = 0; i < table->num_rows(); i++) {
//     // Another simplification in this example is that we assume that there are
//     // no null entries, e.g. each row is fill with valid values.
//     int64_t turnover = turnovers->Value(i);
//     std::cout << turnover << "\n";
//   }
  auto column_iterator = tidesurf::RecordTableStringColumnIterator(*record_table, 0);
  std::cout << "passhere\n";
  // for (int64_t i = 0; i < record_table->NumRows(); i ++) {
  //     std::string str = column->GetString(i);
  //     std::cout << str << "\n";
  // }
  while (column_iterator.HasNext()) {
    std::string str = column_iterator.Next();
    std::cout << str << "\n";
  }
  delete record_table;
  return arrow::Status::OK();
}

// #3: Read only a single RowGroup of the parquet file
void read_single_rowgroup() {
  std::cout << "Reading first RowGroup of parquet-arrow-example.parquet" << std::endl;
  std::shared_ptr<arrow::io::ReadableFile> infile;
  PARQUET_ASSIGN_OR_THROW(
      infile,
      arrow::io::ReadableFile::Open("parquet-arrow-example.parquet",
                                    arrow::default_memory_pool()));

  std::unique_ptr<parquet::arrow::FileReader> reader;
  PARQUET_THROW_NOT_OK(
      parquet::arrow::OpenFile(infile, arrow::default_memory_pool(), &reader));
  std::shared_ptr<arrow::Table> table;
  PARQUET_THROW_NOT_OK(reader->RowGroup(0)->ReadTable(&table));
  std::cout << "Loaded " << table->num_rows() << " rows in " << table->num_columns()
            << " columns." << std::endl;
}

// #4: Read only a single column of the whole parquet file
void read_single_column() {
  std::cout << "Reading first column of parquet-arrow-example.parquet" << std::endl;
  std::shared_ptr<arrow::io::ReadableFile> infile;
  PARQUET_ASSIGN_OR_THROW(
      infile,
      arrow::io::ReadableFile::Open("parquet-arrow-example.parquet",
                                    arrow::default_memory_pool()));

  std::unique_ptr<parquet::arrow::FileReader> reader;
  PARQUET_THROW_NOT_OK(
      parquet::arrow::OpenFile(infile, arrow::default_memory_pool(), &reader));
  std::shared_ptr<arrow::ChunkedArray> array;
  PARQUET_THROW_NOT_OK(reader->ReadColumn(0, &array));
  PARQUET_THROW_NOT_OK(arrow::PrettyPrint(*array, 4, &std::cout));
  std::cout << std::endl;
}

// #5: Read only a single column of a RowGroup (this is known as ColumnChunk)
//     from the Parquet file.
void read_single_column_chunk() {
  std::cout << "Reading first ColumnChunk of the first RowGroup of "
               "parquet-arrow-example.parquet"
            << std::endl;
  std::shared_ptr<arrow::io::ReadableFile> infile;
  PARQUET_ASSIGN_OR_THROW(
      infile,
      arrow::io::ReadableFile::Open("parquet-arrow-example.parquet",
                                    arrow::default_memory_pool()));

  std::unique_ptr<parquet::arrow::FileReader> reader;
  PARQUET_THROW_NOT_OK(
      parquet::arrow::OpenFile(infile, arrow::default_memory_pool(), &reader));
  std::shared_ptr<arrow::ChunkedArray> array;
  PARQUET_THROW_NOT_OK(reader->RowGroup(0)->Column(0)->Read(&array));
  PARQUET_THROW_NOT_OK(arrow::PrettyPrint(*array, 4, &std::cout));
  std::cout << std::endl;
}

int main(int argc, char** argv) {
    tidesurf::start_server();
    return 0;
}