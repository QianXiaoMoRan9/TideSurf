#include "tidesurf/interval_record.h"

using namespace tidesurf;

IntervalRecord::IntervalRecord(Price avg_price, uint64_t turnover, double volume) : avg_price_(avg_price),
                                                                                    turnover_(turnover),
                                                                                    volume_(volume),
                                                                                    percentage_(0) {}

IntervalRecord::IntervalRecord(Price avg_price, uint64_t turnover, double volume, double percentage) : avg_price_(
        avg_price),
                                                                                                       turnover_(
                                                                                                               turnover),
                                                                                                       volume_(volume),
                                                                                                       percentage_(
                                                                                                               percentage) {}

Price IntervalRecord::GetAvgPrice() const {
    return avg_price_;
}

uint64_t IntervalRecord::GetTurnover() const {
    return turnover_;
}

double IntervalRecord::GetVolume() const {
    return volume_;
}

double IntervalRecord::GetPercentage() const {
    return percentage_;
}

void IntervalRecord::SetPrice(Price price) {
    avg_price_ = price;
}

void IntervalRecord::SetTurnover(uint64_t turnover) {
    turnover_ = turnover;
}

void IntervalRecord::SetVolume(double volume) {
    volume_ = volume;
}

void IntervalRecord::SetPercentage(double percentage) {
    percentage_ = percentage;
}



