#pragma once
#include <cstdint>
#include <iostream>
namespace tidesurf {

class Stock {
public:
Stock(float price, std::string code, std::string name) {
    price_ = price;
    code_ = code;
    name_ = name;
}

private:
    float price_;
    std::string name_;
    std::string code_;
};

}

