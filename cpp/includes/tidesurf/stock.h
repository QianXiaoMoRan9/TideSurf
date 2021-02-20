#pragma once
#include <cstdint>
#include <iostream>
#include <arrow/api.h>
#include "tidesurf/split_share.h"
#include "tidesurf/iso_datetime.h"
namespace tidesurf
{

    class Stock
    {
    public:
        Stock(std::string code, std::string name)
            : code_(code),
              name_(name)
        {
            price_ = -1.0;
        }

        double GetPrice() {
            return price_;
        }

        void SetPrice(double price) {
            price_ = price;
        }

        std::string GetCode() {
            return code_;
        }

        std::string GetName() {
            return name_;
        }

    private:
        double price_;
        std::string name_;
        std::string code_;
    };

    class AStock : public Stock
    {
        public:
        AStock(std::string code, std::string name, std::string abbreviation, AStockSplitShare split_share) 
        : Stock(code, name), abbreviation_(abbreviation), split_share_records_(split_share) {

        }

        std::string GetAbbreviation() {
            return abbreviation_;
        }

        private:
        std::string abbreviation_;
        AStockSplitShare split_share_records_;
    };

} // namespace tidesurf
