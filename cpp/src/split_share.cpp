#include "tidesurf/split_share.h"
using namespace tidesurf;

SplitShareRecord::SplitShareRecord(
    double pre_split_adjust_factor,
    double post_split_adjust_factor,
    ISODate date) : pre_split_adjust_factor_(pre_split_adjust_factor),
                    post_split_adjust_factor_(post_split_adjust_factor),
                    date_(date)
{
}

bool SplitShareRecord::operator<(const SplitShareRecord &rhs) const {
    return (this->GetDate() < rhs.GetDate() 
            || this->GetPreSplitAdjustFactor() < rhs.GetPreSplitAdjustFactor()
            || this->GetPostSplitAdjustFactor() < rhs.GetPostSplitAdjustFactor());
}

bool compare_split_records_descending(const SplitShareRecord &lfs, const SplitShareRecord &rhs) {
    return !(lfs < rhs);
}

AStockSplitShare::AStockSplitShare(
    const std::string table_file_path)
{
    RecordTable *table = new RecordTable(
        SINA_A_STOCK_SPLIT_SHARE_PARQUET_TABLE_SCHEMA,
        table_file_path
    );
    RecordTableStringColumnIterator *code_iterator = new RecordTableStringColumnIterator(*table, 0);
    RecordTableInt64ColumnIterator *year_iterator = new RecordTableInt64ColumnIterator(*table, 3);
    RecordTableInt64ColumnIterator *month_iterator = new RecordTableInt64ColumnIterator(*table, 4);
    RecordTableInt64ColumnIterator *day_iterator = new RecordTableInt64ColumnIterator(*table, 5);
    RecordTableDoubleColumnIterator *pre_split_iterator = new RecordTableDoubleColumnIterator(*table, 12);
    RecordTableDoubleColumnIterator *post_split_iterator = new RecordTableDoubleColumnIterator(*table, 13);
    
    while (code_iterator->HasNext()) {
        std::string code = code_iterator->Next();
        int64_t year = year_iterator->Next();
        int64_t month = month_iterator->Next();
        int64_t day = day_iterator->Next();
        double pre_split = pre_split_iterator->Next();
        double post_split = post_split_iterator->Next();
        SplitShareRecord record = *(new SplitShareRecord(pre_split, post_split, *(new ISODate(year, month, day))));
        if (split_record_map_.count(code) == 0) {
            split_record_map_.emplace(code, *(new std::list<SplitShareRecord>()));
            pre_split_iterator_map_.emplace(code, split_record_map_.begin());
            post_split_iterator_map_.emplace(code, split_record_map_.end());
        }
        split_record_map_[code].push_back(record);
    }

    for (auto dict_iterator : split_record_map_)
    {
        dict_iterator.second.sort(compare_split_records_descending);
        pre_split_iterator_map_[dict_iterator.first] = dict_iterator.second.begin();
        post_split_iterator_map_[dict_iterator.first] = --dict_iterator.second.end();
    }


    delete code_iterator, year_iterator, month_iterator, day_iterator;
    delete pre_split_iterator, post_split_iterator;
    delete table;
}

std::unordered_map<std::string, double> AStockSplitShare::AdvancePreSplitForDate(
    std::unordered_map<std::string, double> &result,
    ISODate date)
{
    for (auto dict_iterator : pre_split_iterator_map_)
    {
        std::string code = dict_iterator.first;
        auto iterator = dict_iterator.second;
        if (date == (*iterator).GetDate()) {
            result.emplace(code, (*iterator).GetPreSplitAdjustFactor());
            pre_split_iterator_map_[code] ++;
        }
    }
    return result;
}
std::unordered_map<std::string, double> AStockSplitShare::AdvancePostSplitForDate(
    std::unordered_map<std::string, double> &result,
    ISODate date)
{
    for (auto dict_iterator : post_split_iterator_map_)
    {
        std::string code = dict_iterator.first;
        auto iterator = dict_iterator.second;
        if (date == (*iterator).GetDate()) {
            result.emplace(code, (*iterator).GetPostSplitAdjustFactor());
            post_split_iterator_map_[code] ++;
        }
    }
    return result;
}
