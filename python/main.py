from collections import namedtuple

from event import EventHandler
from gildedrose import update_quality
from item import Item
from report import Report

DataWithTimestamp = namedtuple("DataWithTimestamp", ["data", "time"])
# Note: other group had a lift method to apply a function to data


class Functor:
    def __init__(self, data_with_timestamp):
        self.data_with_timestamp = data_with_timestamp

    def map_just_data(self, function):
        # either, map left, right or all like below
        mapped_value = function(self.data_with_timestamp.data)
        new_value = DataWithTimestamp(mapped_value, self.data_with_timestamp.time)
        return Functor(new_value)

    def map(self, function):
        mapped_value = function(self.data_with_timestamp)
        new_value = DataWithTimestamp(mapped_value, self.data_with_timestamp.time)
        return Functor(new_value)


class MainEventHandler(EventHandler):
    def on_database_ready(self, time, database):
        items = []
        for name, quality, sell_in in database.get_items():
            items.append(Item(name, quality, sell_in))
        value_for_functor = DataWithTimestamp(items, time)
        return Functor(value_for_functor)

    def on_update(self, items: Functor):
        return items.map_just_data(update_quality)

    def on_report(self, items: Functor):
        return items.map_just_data(lambda x: str(Report(x)))

    def on_write_file(self, text: Functor):
        def write(data_with_timestamp):
            text, time = data_with_timestamp
            filename_we_would_like_to_have = f"report@{time.date()}.txt"
            with open(filename_we_would_like_to_have, "w") as f:
                f.write(text)

        text.map(write)


if __name__ == "__main__":
    MainEventHandler().run_handler()
