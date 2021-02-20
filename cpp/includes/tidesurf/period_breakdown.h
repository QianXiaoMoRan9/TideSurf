#pragma once 
#include <map>
#include <list>
#include <arrow/api.h>
#include "tidesurf/price.h"
#include "tidesurf/tidesurf_types.h"
#include "tidesurf/iso_datetime.h"

namespace tidesurf {
    class BreakdownRecord {
        public:
        BreakdownRecord(int64_t price_int, int64_t price_float, int64_t num_share, double share_percentage) 
        : price_(*(new Price(price_int, price_float, POSITIVE))), num_share_(num_share), share_percentage_(share_percentage)
        {
        }
        private:
            Price price_;
            int64_t num_share_;
            double share_percentage_;
    };

    class Breakdown {
        public:
        Breakdown(RecordPeriod record_period) : record_period_(record_period)
        {
            record_map_ = *(new std::map<ISODatetime, std::list<BreakdownRecord>>());
        }   

        void AddRecord(ISODatetime date, int64_t price_int, int64_t price_float, int64_t num_share, double share_percentage) {
            if (record_map_.count(date) == 0) {
                record_map_.emplace(date, *(new std::list<BreakdownRecord>()));
            }

            record_map_[date].push_back(*(new BreakdownRecord(price_int, price_float, num_share, share_percentage)));
        }

        void SortRecordMapByPrice() {
            for (auto iterator = record_map_.begin(); iterator != record_map_.end(); ++iterator) {
                iterator->second.sort();
            }
        }

        private:
            RecordPeriod record_period_;
            std::map<ISODatetime, std::list<BreakdownRecord>> record_map_;
    };

}
