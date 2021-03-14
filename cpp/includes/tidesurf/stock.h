#pragma once

#include <cstdint>
#include <iostream>
#include <utility>
#include <unordered_map>
#include <list>
#include <arrow/api.h>
#include "tidesurf/tidesurf_types.h"
#include "tidesurf/interval_record.h"
#include "tidesurf/price.h"
#include "tidesurf/split_share.h"
#include "tidesurf/iso_datetime.h"

namespace tidesurf {

    /**
     * 
     * Major stock object that holds SHARABLE data
     * 
     * This includes the current statistics, and historical statistics
     * 
     * 
     * 
     */
    class Stock {
    public:
        Stock(std::string code, std::string name, std::string abbreviation = "N/A");


        Price GetPrice() const;
        std::string GetCode() const;
        std::string GetName() const;
        std::string GetAbbreviation() const;


        void SetPrice(Price price);
        void SetName(std::string name);
        void SetAbbreviation(std::string abbrev);


    private:
        Price price_;
        std::string name_;
        std::string code_;
        std::string abbreviation_;
        std::unordered_map<IntervalType, std::list<IntervalRecord>> interval_record_map_;


    };

    class AStock : public Stock {
    public:
        AStock(std::string code, std::string name, std::string abbreviation, AStockSplitShare split_share);

    private:
        AStockSplitShare split_share_records_;
    };

} // namespace tidesurf
