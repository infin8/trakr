from twisted.application.service import ServiceMaker

Tracking = ServiceMaker(
    "trakr simple http tracking",
    "trakr.tap",
    "tracking - unsweetened",
    "trakr")
