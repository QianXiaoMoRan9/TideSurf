#pragma once
#include <unordered_map>
#include <list>
#include <arrow/api.h>
#include "tidesurf/globals.h"
#include "tidesurf/record_table.h"
#include "tidesurf/iso_date.h"

namespace tidesurf
{

    class SplitShareRecord
    {
    public:
        SplitShareRecord(double pre_split_adjust_factor, double post_split_adjust_factor, ISODate date);

        bool operator < (const SplitShareRecord &rhs) const;

        double GetPreSplitAdjustFactor() const
        {
            return pre_split_adjust_factor_;
        }

        double GetPostSplitAdjustFactor() const
        {
            return post_split_adjust_factor_;
        }

        ISODate GetDate() const
        {
            return date_;
        }

    private:
        double pre_split_adjust_factor_;
        double post_split_adjust_factor_;
        ISODate date_;
    };

    bool inversely_compare_split_records(const SplitShareRecord &lfs, const SplitShareRecord &rhs);

    class AStockSplitShare
    {
    public:
        AStockSplitShare(const std::string table_file_path);
        std::unordered_map<std::string, double> AdvancePreSplitForDate(
            std::unordered_map<std::string, double> &result,
            ISODate date);
        std::unordered_map<std::string, double> AdvancePostSplitForDate(
            std::unordered_map<std::string, double> &result,
            ISODate date);
        void ResetIterator();

    private:
        std::unordered_map<std::string, std::list<SplitShareRecord>> split_record_map_;
        std::unordered_map<std::string, std::list<SplitShareRecord>::iterator> pre_split_iterator_map_;
        std::unordered_map<std::string, std::list<SplitShareRecord>::iterator> post_split_iterator_map_;
    };
} // namespace tidesurf
