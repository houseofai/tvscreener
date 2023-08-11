import datetime
import re
import time

import jinja2
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from tqdm import tqdm

import data

xpath_column_setup = "/html/body/div[4]/div/div[2]/div[11]"
xpath_filters = "/html/body/div[4]/div/div[2]/div[11]"

template_field = """
# ----------------------
# Generated file
# {{ now() }}
# ----------------------
from tvscreener.field import Field


class {{ name }}Field(Field):{% for key, v in enum_values.items() %}
    {{ key }} = '{{ v.label }}', '{{ v.field_name }}', '{{ v.format }}', {{ v.interval }}, {{ v.historical }}{% endfor %}
    
"""
template_filters = """
# ----------------------
# Generated file
# {{ now() }}
# ----------------------
from enum import Enum


class {{ name }}(Enum):{% for key, v in enum_values.items() %}
    {{ key }} = '{{ v }}'{% endfor %}
    
"""

computed_reco_fields = ['ADX',
                        'AO',
                        'BB.lower',
                        'BB.upper',
                        'CCI20',
                        'EMA10',
                        'EMA100',
                        'EMA20',
                        'EMA200',
                        'EMA30',
                        'EMA5',
                        'EMA50',
                        'Ichimoku.BLine',
                        'MACD.macd',
                        'Mom',
                        'P.SAR',
                        'RSI',
                        'RSI7',
                        'float_shares_outstanding',
                        'SMA10',
                        'SMA100',
                        'SMA20',
                        'SMA200',
                        'SMA30',
                        'SMA5',
                        'SMA50',
                        'Stoch.K',
                        'Stoch.RSI.K',
                        'total_shares_outstanding_fundamental',
                        'Value.Traded',
                        'W.R'
                        ]

historical_fields = ["ADX+DI",
                     "ADX-DI",
                     "AO",
                     "AO",  # Second time
                     "CCI20",
                     "Mom",
                     "RSI7",
                     "RSI",
                     "Stoch.K",
                     "Stoch.D",
                     ]


def is_historical_field(field_name):
    return field_name in historical_fields


def is_recommendation(field_value):
    return field_value.endswith(' N') or field_value.endswith(' S') or field_value.endswith(' B')


def click_on(driver, xpath):
    WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()


def get_format(technical_label, field_value):
    field_type_ = None
    if "USD" in field_value:
        field_type_ = "currency"
    elif "%" in field_value:
        field_type_ = "percent"
    elif field_value.endswith("M"):
        field_type_ = "number_group"
    elif field_value.endswith("K"):
        field_type_ = "number_group"
    elif field_value in ['Sell', 'Buy']:
        field_type_ = "rating"
    elif is_recommendation(field_value):
        if technical_label in computed_reco_fields:
            field_type_ = "computed_recommendation"
        else:
            field_type_ = "recommendation"
    elif field_value.endswith("B"):  # Order matters to avoid matching with "Buy" recommendation
        field_type_ = "number_group"
    elif "." in field_value:
        try:
            float(field_value.replace('−', '-'))
            if len(field_value.split(".")[1]) == 2:
                field_type_ = "round"
            else:
                field_type_ = "float"
        except:
            pass
    elif "—" in field_value or field_value == "":
        field_type_ = "missing"
    elif field_value.count('-'):
        field_type_ = "date"
    elif bool(re.match('[a-zA-Z\s]+$', field_value)):
        field_type_ = "text"
    return field_type_


def _start_window(url_):
    # proxy = Proxy()
    # proxy.setHttpProxy("https://scanner.tradingview.com/:8080")
    driver = webdriver.Firefox()  # proxy=proxy)

    driver.get(url_)
    driver.maximize_window()
    # driver.implicitly_wait(5)

    # Waiting for the Google popup to load
    time.sleep(2)

    # Google popup
    google_iframe_xpath = '/html/body/div[3]/div[3]/div[2]/div[4]/div/iframe'
    frame = driver.find_element_by_xpath(google_iframe_xpath)
    driver.switch_to.frame(frame)
    # Close the Google popup
    google_closebtn_xpath = '//*[@id="close"]'
    click_on(driver, google_closebtn_xpath)

    driver.switch_to.default_content()
    time.sleep(1)
    return driver


def get_xpath_filter_field(i):
    return f"/html/body/div[10]/div/div/div/div[3]/div[1]/div/div/div[{i}]/div[2]/div/span"


def get_xpath_field_name(i):
    return f"/html/body/div[10]/div/div/div/div[3]/div[1]/div/div/div[{i}]/div[1]"


def get_xpath_filter_value(i):
    return f"/html/body/div[10]/div/div/div/div[4]/div/div[1]/div[{i}]/label/span"


def get_field_values(driver):
    fields = driver.find_element_by_xpath("/html/body/div[10]/div/div/div/div[4]/div/div[1]")
    innerHTML = fields.get_attribute('innerHTML')

    soup = BeautifulSoup(innerHTML, "html.parser")
    # get all the spans
    spans = soup.find_all("span", class_="tv-control-checkbox__label")
    fields_values = [span.text for span in spans]
    return fields_values


def scrap_field_values(url_):
    driver = _start_window(url_)
    click_on(driver, xpath_filters)
    reset_all = "/html/body/div[10]/div/div/div/div[2]/div"
    click_on(driver, reset_all)

    fields = {}
    for i in range(1, 10000):
        xpath_field_name = get_xpath_field_name(i)
        print("Search field on xpath: ", xpath_field_name, "...")
        try:
            field_name = driver.find_element_by_xpath(xpath_field_name).text
        except NoSuchElementException as e:
            break

        if field_name is None or field_name == "":
            break

        xpath_field = get_xpath_filter_field(i)

        try:
            click_on(driver, xpath_field)
            fields_values = get_field_values(driver)
            fields[field_name] = fields_values
        except TimeoutException:
            print("TimeoutException on field: ", field_name)
            continue
        except NoSuchElementException:
            print("NoSuchElementException on field: ", field_name)
            continue

    driver.quit()
    return fields


def scrap_columns(url_):
    driver = _start_window(url_)
    click_on(driver, xpath_column_setup)

    fields_attribute = {}
    # Check all the columns
    i = 0
    filters_base_xpath = "/html/body/div[4]/div/div[3]/div/div[2]/div[2]/div[1]"
    print("Checking filters...")
    for i in tqdm(range(1, 1000)):
        filter_base_xpath = filters_base_xpath + f"/div[{i}]"
        technical_label_xpath = filter_base_xpath + "/label"
        label_xpath = filter_base_xpath + "/label/span"
        checkbox_xpath = filter_base_xpath + "/label/label/input"

        try:
            # print(f"Checking: {i} - {checkbox_xpath}")
            checkbox = driver.find_element_by_xpath(checkbox_xpath)
            # Check if not checked
            if not checkbox.is_selected():
                checkbox.click()

            # Technical label
            technical_label = driver.find_element_by_xpath(technical_label_xpath)
            # Label
            label = driver.find_element_by_xpath(label_xpath)
            fields_attribute[technical_label.get_attribute("data-field")] = {"label": label.text}
        except NoSuchElementException as e:
            print(e)
            print(f"Found: {i - 1} filters")
            break

    # Waiting for the columns to load
    time.sleep(3)

    print("Checking columns...")
    for j in tqdm(range(2, i + 1)):
        column_field = f"/html/body/div[4]/div/div[4]/table/tbody/tr[1]/td[{j}]"
        row_value = driver.find_element_by_xpath(column_field)
        technical_label = row_value.get_attribute("data-field-key")

        field_value = row_value.text
        format_ = get_format(technical_label, field_value)
        historical = is_historical_field(technical_label)

        if format_ is None:
            print(f"{technical_label} - |{field_value}| - {format_} - {historical}")
        fields_attribute[technical_label] = {**fields_attribute[technical_label], "format": format_,
                                             "historical": historical}

    driver.quit()
    return fields_attribute


def remove(field, chars):
    for c in chars:
        field = field.replace(c, '')
    return field


def format_field(field: str):
    # If the field starts with a number
    if field[:2].isdigit():
        field = f'{field[2:]}_{field[:2]}'
    elif field[0].isdigit():
        field = f'{field[1:]}_{field[0]}'
    # Remove
    field = remove(field, ['(', ')', ',', '/', '-', ':'])
    field = field.strip()
    # Replace
    field = (field.replace(' ', '_')
             .replace('-', '_')
             .replace('*', 'x')
             .replace('&', 'and')
             .replace('%', 'percent')
             .replace('1m', '1min')
             .replace('5m', '5min')
             .replace('.', '_')
             )
    return field.upper()


def format_fields(dict_):
    # Sort dictionary by keys lower case
    dict_ = {k: dict_[k] for k in sorted(dict_, key=lambda s: format_field(dict_[s]['label'].lower()))}
    new_dict = {}
    for field_name, v in dict_.items():
        label = v.get('label')
        format_ = f'{v.get("format", None)}' if v.get('format', None) else None
        interval = v.get('interval', False)
        historical = v.get('historical', False)
        enum_field = format_field(label)

        new_dict[enum_field] = {
            'label': label,
            'field_name': field_name,
            'format': format_,
            'interval': interval,
            'historical': historical
        }
    return new_dict


def set_intervals(columns):
    columns_w_interval = load_intervals()
    for col in columns_w_interval:
        if col in columns:
            columns[col]['interval'] = True
        else:
            print(f'Column {col} not found in the interval columns')
    return columns


def fill_template(name, columns):
    # Render the template
    template_code = jinja2.Template(template_field)
    template_code.globals['now'] = datetime.datetime.utcnow
    return template_code.render(name=name, enum_values=columns)


def fill_filter_template(classname, columns):
    # Render the template
    template_code = jinja2.Template(template_filters)
    template_code.globals['now'] = datetime.datetime.utcnow
    return template_code.render(name=classname, enum_values=columns)


def load_intervals():
    with open('data/time_intervals.json') as f:
        return data.load(f)['columns']


def load_patterns():
    with open('data/patterns.json') as f:
        return data.load(f)['patterns']


def load_main():
    with open('data/main.json') as f:
        return data.load(f)['main']


def add_patterns_columns(columns):
    patterns = load_patterns()
    for pattern in patterns:
        columns[pattern] = {
            'label': pattern,
            'field_name': pattern,
            'format': 'bool',
            'interval': False,
            'historical': False
        }
    return columns


def add_main_columns(columns):
    main_columns = load_main()
    for col in main_columns:
        # Label: Upper case the first letter of each word
        label = ' '.join([word[0].upper() + word[1:] for word in col.split('_')])
        columns[col] = {
            'label': label,
            'field_name': col,
            'format': 'text',
            'interval': False,
            'historical': False
        }
    return columns


def generate_filter_columns(values):
    newdic = {}
    for value in values:
        if value != 'Any':
            newdic[format_field(value)] = value
    return newdic


def generate_columns(selenium_columns):
    selenium_columns = add_main_columns(selenium_columns)
    selenium_columns = add_patterns_columns(selenium_columns)
    selenium_columns = set_intervals(selenium_columns)
    selenium_columns = format_fields(selenium_columns)
    return selenium_columns


def write(filename, generated_template):
    with open(f'code/{filename}.py.generated', 'w') as fp:
        fp.write(generated_template)
