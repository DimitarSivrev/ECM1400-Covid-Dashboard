from covid_news_handling import news_API_request
from covid_news_handling import update_news
from covid_news_handling import schedule_news_updates
from covid_news_handling import removed_news_function

def test_news_API_request():
    assert news_API_request()
    assert news_API_request('Covid COVID-19 coronavirus') == news_API_request()

def test_update_news():
    update_news('test')

def test_schedule_news_updates():
    schedule_news_updates(update_interval=10, update_name='update test')
    schedule_news_updates(update_interval=10, update_name='update test', type = 'repeating')

def test_remove_news_function():
    removed_news_function('Test')