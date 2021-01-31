#pragma once
#include <cstdint>
#include <iostream>
#include <arrow/api.h>

namespace tidesurf
{

    class Stock
    {
    public:
        Stock(std::string code, std::string name, std::string abbreviation)
            : code_(code),
              name_(name),
              abbreviation_(abbreviation)
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

        std::string GetAbbreviation() {
            return abbreviation_;
        }

    private:
        double price_;
        std::string name_;
        std::string code_;
        std::string abbreviation_;
    };

} // namespace tidesurf
