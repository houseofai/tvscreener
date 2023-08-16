from typing import Type

import numpy as np
import pandas as pd

from tvscreener import Field, millify, ScreenerDataFrame, StockField
from tvscreener.field import Rating
import tvscreener.ta as ta

buy_char = "&#x2303; B"
sell_char = "&#x2304; S"
neutral_char = "- N"
red = "color:rgb(255, 23, 62);"
green = "color:rgb(0, 169, 127);"


def beautify(df, specific_fields):
    df = Beautify(df, specific_fields).df
    return df


def _get_recommendation(rating):
    if rating < 0:
        return Rating.SELL
    elif rating == 0:
        return Rating.NEUTRAL
    elif rating > 0:
        return Rating.BUY


def _percent_colors(row):
    return red if row.startswith("-") else green  # Green


def _rating_colors(v):
    if v.endswith(buy_char):
        return 'color:rgb(41, 98, 255);'  # Blue
    elif v.endswith(sell_char):
        return 'color:rgb(255, 74, 104);'  # Red
    else:
        return 'color:rgb(157, 178, 189);'  # Gray


def _rating_letter(rating: Rating):
    if rating == Rating.BUY:
        return buy_char
    elif rating == Rating.SELL:
        return sell_char
    else:
        return neutral_char


class Beautify:
    def __init__(self, sdf: ScreenerDataFrame, specific_fields: Type[Field]):
        sdf.set_technical_columns(only=True)
        self.df = sdf.copy()
        self.df_beauty = self.df.style

        for field in specific_fields:
            if field.field_name in self.df.columns:
                self._format_column(field)

        # for column in self.df.columns:
        #    # Find the enum with the column name
        #    specific_field = specific_fields.get_by_label(specific_fields, column)
        #    if specific_field is not None and specific_field.format is not None:
        #        # self._copy_column(column)
        #        # fn = self.fn_mappings.get(format_)
        #        self._format_column(specific_field)

    def _format_column(self, field):
        fmt = field.format
        if fmt == 'bool':
            self._to_bool(field)
        elif fmt == 'rating':
            self._rating(field)
        elif fmt == 'round':
            self._round(field)
        elif fmt == 'percent':
            self._percent(field)
        elif field.has_recommendation():
            self._recommendation(field)
        elif fmt == 'computed_recommendation':
            self._computed_recommendation(field)
        elif field.format == 'text':
            # TODO
            pass
        elif field.format == 'date':
            # TODO
            pass
        elif field.format == 'missing':
            # TODO
            pass
        elif field.format == 'currency':
            self._round(field)
            #self.df[field.field_name] = self.df[field.field_name].apply(lambda x: x if not np.isnan(x) else "--")
            self._number_group(field)
            self._currency(field)
        elif field.format == 'float':
            # TODO
            pass
        elif field.format == 'number_group':
            self._replace_nan(field)
            self._number_group(field)
        else:
            print(f"Unknown format: {field.format} for column: {field}")

    def _rating(self, field: Field):
        self.df[field.field_name] = self.df[field.field_name].apply(lambda x: Rating.find(x).label)

    def _recommendation(self, field):
        self.df[field.field_name] = self.df.apply(
            lambda x: f"{x[field.field_name]} {_rating_letter(_get_recommendation(x[field.get_rec_field()]))}", axis=1)
        self.df_beauty = self.df_beauty.applymap(_rating_colors, subset=pd.IndexSlice[:, [field.field_name]])

    def _currency(self, field):
        self.df[field.field_name] = self.df.apply(
            lambda x: f"{x[field.field_name]} {x[StockField.CURRENCY.field_name]}" if x[field.field_name] != "--" else
            x[field.field_name], axis=1)

    def _number_group(self, field):
        self.df[field.field_name] = self.df[field.field_name].apply(lambda x: millify(x) if x != "--" else x)

    def _percent(self, field):
        self.df[field.field_name] = self.df[field.field_name].apply(lambda x: f"{x:.2f}%" if not np.isnan(x) else "--")
        self.df_beauty = self.df_beauty.applymap(_percent_colors, subset=pd.IndexSlice[:, [field.field_name]])

    def _round(self, field):
        self.df[field.field_name] = self.df[field.field_name].apply(
            lambda x: round(x, 2) if not np.isnan(x) else "--")

    def _copy_column(self, field):
        raw_name = field.field_name + " raw"
        self.df[raw_name] = self.df[field.field_name]

    def _replace_nan(self, field):
        self.df[field.field_name] = self.df[field.field_name].fillna(0)

    def _to_bool(self, field):
        self.df[field.field_name] = self.df[field.field_name].apply(lambda x: True if x == 'true' else False)
        self.df[field.field_name] = self.df[field.field_name].astype(bool)

    def _computed_recommendation(self, field):
        # FIXME Column name can have update mode
        if field.field_name == "ADX":
            self.df[field.field_name] = self.df.apply(
                lambda
                    x: f"{x[field.field_name]} {_rating_letter(ta.adx(x['ADX'], x['ADX-DI'], x['ADX+DI'], x['ADX-DI[1]'], x['ADX+DI[1]']))}",
                axis=1)
            self.df_beauty = self.df_beauty.applymap(_rating_colors, subset=pd.IndexSlice[:, [field.field_name]])
        elif field.field_name == "AO":
            self.df[field.field_name] = self.df.apply(
                lambda x: f"{x[field.field_name]} {_rating_letter(ta.ao(x['AO'], x['AO[1]'], x['AO[2]']))}",
                axis=1)
            self.df_beauty = self.df_beauty.applymap(_rating_colors, subset=pd.IndexSlice[:, [field.field_name]])
        elif field.field_name == "BB.lower":
            self.df[field.field_name] = self.df.apply(
                lambda x: f"{x[field.field_name]} {_rating_letter(ta.bb_lower(x[field.field_name], x['close']))}",
                axis=1)
            self.df_beauty = self.df_beauty.applymap(_rating_colors, subset=pd.IndexSlice[:, [field.field_name]])
        elif field.field_name == "BB.upper":
            self.df[field.field_name] = self.df.apply(
                lambda x: f"{x[field.field_name]} {_rating_letter(ta.bb_upper(x[field.field_name], x['close']))}",
                axis=1)
            self.df_beauty = self.df_beauty.applymap(_rating_colors, subset=pd.IndexSlice[:, [field.field_name]])
