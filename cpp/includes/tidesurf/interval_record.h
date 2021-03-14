
#ifndef TIDESURF_INTERVAL_RECORD_H
#define TIDESURF_INTERVAL_RECORD_H
#pragma once
#include <arrow/api.h>
#include "tidesurf/price.h"

namespace tidesurf {
    class IntervalRecord {
    public:
        IntervalRecord(Price avg_price, uint64_t turnover, double volume);
        IntervalRecord(Price avg_price, uint64_t turnover, double volume, double percentage);
        Price GetAvgPrice() const;
        uint64_t GetTurnover() const;
        double GetVolume() const;
        double GetPercentage() const;

        void SetPrice(Price price);
        void SetTurnover(uint64_t turnover);
        void SetVolume(double volume);
        void SetPercentage(double percentage);


    private:
        Price avg_price_;
        uint64_t turnover_;
        double volume_;
        double percentage_;
    };

}


#endif //TIDESURF_INTERVAL_RECORD_H
