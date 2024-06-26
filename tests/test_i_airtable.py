"""Test functions for Airtable interface functionality.
"""
from datetime import datetime
import os

from pyairtable import Table
import pytest

from aracnid_api import AirtableInterface


DATETIME_TEST_STR = '2020-08-05T12:00:00-04:00'
DATE_TEST_STR = '2020-08-05'

@pytest.fixture(name='air')
def fixture_airtable():
    """Pytest fixture to initialize and return the AirtableInterface object.
    """
    base_id = os.environ.get('AIRTABLE_TEST_BASE_ID')
    return AirtableInterface(base_id=base_id)

def test_init_airtable(air):
    """Test that Airtable Interface was imported successfully.
    """
    assert air

def test_get_base_name(air):
    """Tests retrieving name of the base.
    """
    base_name = air.get_base_name()

    assert base_name
    assert air.base.name
    assert base_name == 'Dev'

def test_get_table(air):
    """Tests retrieving table.
    """
    table_name = 'test_date'
    table = air.get_table(table_name=table_name)

    assert table
    assert isinstance(table, Table)

def test_get_airtable_datetime(air):
    """Tests the datetime processing of Airtable Interface.
    """
    table_name = 'test_date'
    table = air.get_table(table_name=table_name)

    record_id = 'recuaPzY7QvSbysW1'
    record = table.get(record_id)

    assert record
    dtetime = air.get_airtable_datetime(record, 'datetime_field')
    assert dtetime.isoformat() == DATETIME_TEST_STR

def test_get_airtable_datetime_none(air):
    """Tests the datetime processing of Airtable Interface.

    Value of datetime field is None.
    """
    table_name = 'test_date'
    table = air.get_table(table_name=table_name)
    fields = {
        'Name': 'test_get_airtable_datetime_none()'
    }
    record = air.create_record(table, fields)

    assert record
    dtetime = air.get_airtable_datetime(record, 'datetime_field')
    assert dtetime is None

def test_get_airtable_datetime_createdtime(air):
    """Tests the datetime processing of Airtable Interface.
    """
    table_name = 'test_date'
    table = air.get_table(table_name=table_name)

    record_id = 'recuaPzY7QvSbysW1'
    record = table.get(record_id)

    assert record
    dtetime = air.get_airtable_datetime(record, 'createdTime')
    assert isinstance(dtetime, datetime)

def test_get_airtable_date(air):
    """Tests the date processing of Airtable Interface.
    """
    table_name = 'test_date'
    table = air.get_table(table_name=table_name)

    record_id = 'recuaPzY7QvSbysW1'
    record = table.get(record_id)

    assert record
    dtetime = air.get_airtable_date(record, 'date_field')
    assert dtetime.isoformat() == DATE_TEST_STR

def test_create_record(air):
    """Tests creating an airtable record.
    """
    table_name = 'test_date'
    table = air.get_table(table_name=table_name)

    field_name = 'Name'
    field_value = "test_create_record()"
    fields = {
        field_name: field_value
    }
    record = air.create_record(table, fields)

    assert record
    assert record['fields'][field_name] == field_value

def test_match_record(air):
    """Tests matching an airtable record.
    """
    record_id = 'recuaPzY7QvSbysW1'

    table_name = 'test_date'
    table = air.get_table(table_name=table_name)

    field_name = 'Name'
    field_value = "test_record"
    record = air.match_record(table, field_name=field_name, field_value=field_value)

    assert record
    assert record['id'] == record_id

def test_match_record_with_apostrophes(air):
    """Tests matching an airtable record.
    """
    record_id = 'recnWXHPUSw0uXJRe'

    table_name = 'test_date'
    table = air.get_table(table_name=table_name)

    field_name = 'Name'
    field_value = "apostrophe's test"
    record = air.match_record(table, field_name=field_name, field_value=field_value)

    assert record
    assert record['id'] == record_id

def test_match_record_with_quotations(air):
    """Tests matching an airtable record.
    """
    record_id = 'rec5OKqfMl6HbBIGm'

    table_name = 'test_date'
    table = air.get_table(table_name=table_name)

    field_name = 'Name'
    field_value = 'quotations "test"'
    record = air.match_record(table, field_name=field_name, field_value=field_value)

    assert record
    assert record['id'] == record_id

def test_update_record(air):
    """Tests updating an airtable record.
    """
    table_name = 'test_date'
    table = air.get_table(table_name=table_name)

    field_name = 'Name'
    field_value = "test_create_record()"
    record = air.match_record(table, field_name=field_name, field_value=field_value)

    new_field_value = 'test_update_record()'
    fields = {
        field_name: new_field_value
    }

    record = air.update_record(table, record['id'], fields)

    assert record
    assert record['fields'][field_name] == new_field_value

def test_delete_record(air):
    """Tests deleting an airtable record.
    """
    table_name = 'test_date'
    table = air.get_table(table_name=table_name)

    field_name = 'Name'
    field_value = "test_update_record()"
    record = air.match_record(table, field_name=field_name, field_value=field_value)
    record_id = record['id']

    record = air.delete_record(table, record_id)

    assert record
    assert record['id'] == record_id
