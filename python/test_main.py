import datetime
from itertools import cycle
from unittest.mock import mock_open, patch

from main import MainEventHandler


def test_run_handler(monkeypatch, file_regression, mocker):
    # for the purpose of this kata more primitive patching would suffice as well
    def select_n(lst, n=3):
        k = len(lst) // n
        return lst[::k]

    monkeypatch.setattr("database.sample", select_n)

    def cycler():
        values = cycle([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.99, 0.999])

        def nextvalue():
            return next(values)

        return nextvalue

    monkeypatch.setattr("pricing.random", cycler())

    # monkeypatch.setattr('event.datetime.today', lambda x: datetime.datetime(2022, 4, 26))
    # TBD: Why does above not work but below does?
    p = mocker.patch("event.datetime")
    p.today.return_value = datetime.datetime(2022, 4, 26)

    with patch("main.open", mock_open(), create=True) as mock:
        MainEventHandler().run_handler()

    filename = "report@2022-04-26.txt"
    # filename = "report.txt"
    mock.assert_called_with(filename, "w")

    file_regression.check(mock.return_value.write.call_args[0][0])
