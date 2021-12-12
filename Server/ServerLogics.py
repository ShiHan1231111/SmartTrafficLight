def is_time_to_capture(remaining_time, start_capture_time):
    return start_capture_time <= remaining_time


def no_data_fetched(red001_traffic, red002_traffic):
    return red001_traffic == "WAITING" or red002_traffic == "WAITING"


def all_data_fetched(red001_traffic, red002_traffic):
    return red001_traffic != "WAITING" and red002_traffic != "WAITING" \
           and red001_traffic != "ACK DATA RECEIVE" and red002_traffic != "ACK DATA RECEIVE"


def only_road1_data_is_fetched(red001_traffic, red002_traffic):
    return red001_traffic != "WAITING" and red002_traffic == "WAITING"


def only_road2_data_is_fetched(red001_traffic, red002_traffic):
    return red002_traffic != "WAITING" and red001_traffic == "WAITING"


def both_roads_have_no_car(road_RED002, road_RED001):
    return road_RED002 == 0 and road_RED001 == 0


def road1_have_no_car_but_road2_have(TFFC_RED001_, TFFC_RED002_):
    return TFFC_RED001_ == 0 and TFFC_RED002_ > 0


def both_side_is_almost_equal_or_road2_no_car(road_RED001, road_RED002, difference_between_two_road):
    return (abs(road_RED001 - road_RED002) <= difference_between_two_road) or (road_RED002 == 0 and road_RED001 != 0)
