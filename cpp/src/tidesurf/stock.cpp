#include "tidesurf/stock.h"

using namespace tidesurf;

Stock::Stock(std::string code, std::string name, std::string abbreviation) : code_(std::move(code)),
                                                   name_(std::move(name)),
                                                   abbreviation_(std::move(abbreviation)),
                                                   price_(Price(-1.0, 100)) {
}

Price Stock::GetPrice() const {
    return price_;
}


std::string Stock::GetCode() const {
    return code_;
}

std::string Stock::GetName() const {
    return name_;
}

std::string Stock::GetAbbreviation() const {
    return abbreviation_;
}

void Stock::SetName(std::string name) {
    name_ = std::move(name);
}
void Stock::SetPrice(Price price) {
    price_ = price;
}
void Stock::SetAbbreviation(std::string abbrev) {
    abbreviation_ = std::move(abbrev);
}

AStock::AStock(std::string code, std::string name, std::string abbreviation, AStockSplitShare split_share)
        : Stock(std::move(code), std::move(name), std::move(abbreviation)),
          split_share_records_(std::move(split_share)) {

}