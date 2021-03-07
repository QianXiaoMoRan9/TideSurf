#pragma once
#include <unordered_map>
#include <list>
#include <arrow/api.h>
#include "tidesurf/globals.h"
#include "tidesurf/record_table.h"
#include "tidesurf/iso_datetime.h"

namespace tidesurf
{

    class SplitShareRecord
    {
    public:
        SplitShareRecord(double backward_split_adjust_factor, double forward_split_adjust_factor, ISODatetime datetime);

        bool operator < (const SplitShareRecord &rhs) const;

        double GetPreSplitAdjustFactor() const;

        double GetPostSplitAdjustFactor() const;

        DeltaISODatetime GetDatetime() const;

    private:
        double backward_split_adjust_factor_;
        double forward_split_adjust_factor_;
        DeltaISODatetime datetime_;
    };

    bool inversely_compare_split_records(const SplitShareRecord &lfs, const SplitShareRecord &rhs);

    class AStockSplitShare
    {
    public:
        AStockSplitShare(const std::string table_file_path);

    private:
        std::unordered_map<std::string, std::list<SplitShareRecord>> split_record_map_;
    };
} // namespace tidesurf
