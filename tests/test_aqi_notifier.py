import vcr
import tempfile
from aqi_notifier import get_sensor_data, parse_sensor_list_file, fetch_aqi
from aqi_notifier.aqi import EPA_AQI
import pytest


def test_parse_sensor_list_file():

    with pytest.raises(ValueError):
        parse_sensor_list_file("non_existent_file.txt")

    with tempfile.NamedTemporaryFile() as fp:
        
        with pytest.raises(ValueError):
            parse_sensor_list_file(fp.name)

        fp.write(b'194203')
        fp.flush()

        sensor_list = parse_sensor_list_file(fp.name)

        assert sensor_list == ['194203']
        
        fp.write(b"\n194204")
        fp.flush()

        sensor_list = parse_sensor_list_file(fp.name)

        assert sensor_list == ['194203', '194204']


def test_get_sensor_data():
    with vcr.use_cassette('tests/fixtures/vcr_cassettes/test_get_sensor_data.yaml'):
        
        sensor_list = [194203]
        api_key = "YOUR OWN API KEY HERE"
        data = get_sensor_data(sensor_list, api_key)

        print(data)
        assert data[0]["sensor"]["name"] == "Bankview"

    
def test_from_pm_raw():
    
    assert EPA_AQI.from_pm_raw(1).aqi == 4
    assert EPA_AQI.from_pm_raw(6).aqi == 25
    assert EPA_AQI.from_pm_raw(82.6).aqi == 165

def test_epa_aqi_status():

    assert EPA_AQI(1).status == "Good"
    assert EPA_AQI(50).status == "Good"
    assert EPA_AQI(51).status == "Moderate"
    assert EPA_AQI(100).status == "Moderate"
    assert EPA_AQI(101).status == "Unhealthy for Sensitive Groups"
    assert EPA_AQI(150).status == "Unhealthy for Sensitive Groups"
    assert EPA_AQI(151).status == "Unhealthy"
    assert EPA_AQI(200).status == "Unhealthy"
    assert EPA_AQI(201).status == "Very Unhealthy"
    assert EPA_AQI(300).status == "Very Unhealthy"
    assert EPA_AQI(301).status == "Hazardous"
    assert EPA_AQI(500).status == "Hazardous"

def test_epa_aqi_recommendations():
    
    assert EPA_AQI(1).recommendations == "Enjoy time outdoors! Breathe the fresh air."
    assert EPA_AQI(50).recommendations == "Enjoy time outdoors! Breathe the fresh air."
    assert EPA_AQI(51).recommendations == "Spend time outside."
    assert EPA_AQI(100).recommendations == "Spend time outside."
    assert EPA_AQI(101).recommendations == "Limit time outdoors."
    assert EPA_AQI(150).recommendations == "Limit time outdoors."
    assert EPA_AQI(151).recommendations == "Exercise caution if you need to go outside today."
    assert EPA_AQI(200).recommendations == "Exercise caution if you need to go outside today."
    assert EPA_AQI(201).recommendations == "Health alert! Severely limit outdoor activitie"
    assert EPA_AQI(300).recommendations == "Health alert! Severely limit outdoor activitie"
    assert EPA_AQI(301).recommendations == "It's fine. You are a cartoon dog drinking coffee while being engulfed in flames."


# Calgary sensors
def test_fetch_aqi():

    sensor_list = [194203, 180571]
    api_key = "YOUR OWN API KEY HERE"

    with vcr.use_cassette('tests/fixtures/vcr_cassettes/test_fetch_aqi_calgary.yaml'):
        aqi = fetch_aqi(sensor_list, api_key)

        assert aqi.aqi == 0
        assert aqi.status == "Good"
        assert aqi.recommendations == "Enjoy time outdoors! Breathe the fresh air."

# Padova sensors
def test_fetch_aqi():

    sensor_list = [157049, 26677, 157035]
    api_key = "YOUR OWN API KEY HERE"

    with vcr.use_cassette('tests/fixtures/vcr_cassettes/test_fetch_aqi_padova.yaml'):
        aqi = fetch_aqi(sensor_list, api_key)

        assert aqi.aqi == 30
        assert aqi.status == "Good"
        assert aqi.recommendations == "Enjoy time outdoors! Breathe the fresh air."