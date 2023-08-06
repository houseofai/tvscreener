import datetime

from selenium import webdriver
import re

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import jinja2

import time

from tqdm import tqdm

template = """
# ----------------------
# Generated file
# {{ now() }}
# ----------------------
from tvscreener.field import Field


class {{ name }}Field(Field):{% for key, v in enum_values.items() %}
    {{ key }} = '{{ v.label }}', '{{ v.field_name }}', '{{ v.format }}', {{ v.interval }}, {{ v.recommendation }}{% endfor %}
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
                        'W.R']


def is_recommendation(field_value):
    return field_value.endswith(' N') or field_value.endswith(' S') or field_value.endswith(' B')


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


def get_columns(url_):
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
    WebDriverWait(driver, 1000000).until(EC.element_to_be_clickable((By.XPATH, google_closebtn_xpath))).click()

    driver.switch_to.default_content()
    time.sleep(1)

    # Open the filter popup
    filter_popup_xpath = "/html/body/div[4]/div/div[3]/div/div[1]"
    WebDriverWait(driver, 1000000).until(EC.element_to_be_clickable((By.XPATH, filter_popup_xpath))).click()

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
        recommendation = format_ is not None and 'recommendation' in format_

        if format_ is None:
            print(f"{technical_label} - |{field_value}| - {format_} - {recommendation}")
        fields_attribute[technical_label] = {**fields_attribute[technical_label], "format": format_,
                                             "recommendation": recommendation}

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
    field = remove(field, ['(', ')', ',', '/', '-'])
    field = field.strip()
    # Replace
    field = field.replace(' ', '_').replace('-', '_').replace('*', 'x').replace('&', 'and').replace('%',
                                                                                                    'percent').replace(
        '1m', '1min').replace('5m', '5min')
    return field.upper()


def generate(dict_):
    # Sort dictionary by keys lower case
    dict_ = {k: dict_[k] for k in sorted(dict_, key=lambda s: format_field(dict_[s]['label'].lower()))}
    new_dict = {}
    for field_name, v in dict_.items():
        label = v.get('label')
        format_ = f'{v.get("format", None)}' if v.get('format', None) else None
        interval = v.get('interval', False)
        recommendation = v.get('recommendation', False)
        enum_field = format_field(label)

        new_dict[enum_field] = {
            'label': label,
            'field_name': field_name,
            'format': format_,
            'interval': interval,
            'recommendation': recommendation
        }
    return new_dict


def generate_template(url, name, original_stock_columns):
    selenium_columns = get_columns(url)
    for k, v in selenium_columns.items():
        if k in original_stock_columns.keys() and 'interval' in original_stock_columns[k].keys():
            selenium_columns[k] = {**v, 'interval:': original_stock_columns[k]['interval']}
        else:
            selenium_columns[k] = {**v, 'interval:': False}

    formatted_columns = generate(selenium_columns)
    # Render the template
    template_code = jinja2.Template(template)
    template_code.globals['now'] = datetime.datetime.utcnow
    return template_code.render(name=name, enum_values=formatted_columns)


def write(filename, generated_template):
    with open(f'../tvscreener/field/{filename}.py', 'w') as fp:
        fp.write(generated_template)
