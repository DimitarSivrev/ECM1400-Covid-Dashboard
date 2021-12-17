from covid_data_handler import parse_csv_data
from covid_data_handler import process_covid_csv_data
from covid_data_handler import covid_API_request
from covid_data_handler import schedule_covid_updates
from covid_data_handler import second_calculator
from covid_data_handler import delete_update
from covid_data_handler import cancel_update
from covid_data_handler import update_covid

def test_parse_csv_data():
    data = parse_csv_data('nation_2021-10-28.csv')
    assert len(data) == 639

def test_process_covid_csv_data():
    last7days_cases , current_hospital_cases , total_deaths = \
        process_covid_csv_data ( parse_csv_data (
            'nation_2021-10-28.csv' ) )
    assert last7days_cases == 240_299
    assert current_hospital_cases == 7_019
    assert total_deaths == 141_544

def test_covid_API_request():
    data = covid_API_request()
    assert isinstance(data, dict)
    assert covid_API_request('Exeter','ltla') == covid_API_request()

def test_schedule_covid_updates():
    schedule_covid_updates(update_interval=10, update_name='update test')
    schedule_covid_updates(update_interval=80, update_name='update test',update_type = 'repeating')

def test_second_calculator():
    seconds = second_calculator("23:11")
    assert isinstance(seconds,int)
    assert seconds <= 86400

def test_delete_update():
    delete_update('test')

def test_cancel_update():
    cancel_update('test')

def test_update_covid():
    update_covid()