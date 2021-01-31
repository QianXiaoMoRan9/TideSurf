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
  std::shared_ptr<arrow::io::ReadableFile> infile;
  PARQUET_ASSIGN_OR_THROW(
      infile,
      arrow::io::ReadableFile::Open("/home/steven/Desktop/Fast500/astock_parquet/2020-12-21/000001.parquet",
                                    arrow::default_memory_pool()));

  std::unique_ptr<parquet::arrow::FileReader> reader;
  PARQUET_THROW_NOT_OK(
      parquet::arrow::OpenFile(infile, arrow::default_memory_pool(), &reader));
  std::shared_ptr<arrow::Table> table;
  PARQUET_THROW_NOT_OK(reader->ReadTable(&table));
  std::cout << "Loaded " << table->num_rows() << " rows in " << table->num_columns()
            << " columns." << std::endl;
    
    
    std::vector<std::shared_ptr<arrow::Field>> schema_vector = {
      arrow::field("ask1", arrow::float64()), 
      arrow::field("ask1_volume", arrow::int64()),
      arrow::field("ask2", arrow::float64()), 
      arrow::field("ask2_volume", arrow::int64()),
      arrow::field("ask3", arrow::float64()), 
      arrow::field("ask3_volume", arrow::int64()),
      arrow::field("ask4", arrow::float64()), 
      arrow::field("ask4_volume", arrow::int64()),
      arrow::field("ask5", arrow::float64()), 
      arrow::field("ask5_volume", arrow::int64()),
      arrow::field("bid1", arrow::float64()), 
      arrow::field("bid1_volume", arrow::int64()),
      arrow::field("bid2", arrow::float64()), 
      arrow::field("bid2_volume", arrow::int64()),
      arrow::field("bid3", arrow::float64()), 
      arrow::field("bid3_volume", arrow::int64()),
      arrow::field("bid4", arrow::float64()), 
      arrow::field("bid4_volume", arrow::int64()),
      arrow::field("bid5", arrow::float64()), 
      arrow::field("bid5_volume", arrow::int64()),
      arrow::field("buy", arrow::float64()), 
      arrow::field("close", arrow::float64()), 
        arrow::field("high", arrow::float64()), 
        arrow::field("low", arrow::float64()), 
        arrow::field("now", arrow::float64()), 
        arrow::field("open", arrow::float64()), 
        arrow::field("sell", arrow::float64()), 
      arrow::field("hour", arrow::int64()),
      arrow::field("minute", arrow::int64()),
      arrow::field("second", arrow::int64()),
      arrow::field("turnover", arrow::int64()),
        arrow::field("volume", arrow::float64()), 
    };
  auto expected_schema = std::make_shared<arrow::Schema>(schema_vector);

  if (!expected_schema->Equals(*table->schema())) {
    // The table doesn't have the expected schema thus we cannot directly
    // convert it to our target representation.
    return arrow::Status::Invalid("Schemas are not matching!");
  }

  // As we have ensured that the table has the expected structure, we can unpack the
  // underlying arrays. For the primitive columns `id` and `cost` we can use the high
  // level functions to get the values whereas for the nested column
  // `cost_components` we need to access the C-pointer to the data to copy its
  // contents into the resulting `std::vector<double>`. Here we need to be care to
  // also add the offset to the pointer. This offset is needed to enable zero-copy
  // slicing operations. While this could be adjusted automatically for double
  // arrays, this cannot be done for the accompanying bitmap as often the slicing
  // border would be inside a byte.

  auto turnovers =
      std::static_pointer_cast<arrow::Int64Array>(table->column(30)->chunk(0));

  for (int64_t i = 0; i < table->num_rows(); i++) {
    // Another simplification in this example is that we assume that there are
    // no null entries, e.g. each row is fill with valid values.
    int64_t turnover = turnovers->Value(i);
    std::cout << turnover << "\n";
  }
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
  std::shared_ptr<arrow::Table> table = generate_table();
  write_parquet_file(*table);
  read_whole_file();
  read_single_rowgroup();
  read_single_column();
  read_single_column_chunk();
}