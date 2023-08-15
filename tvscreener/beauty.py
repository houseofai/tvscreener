from typing import Type

import numpy as np
import pandas as pd

from tvscreener import Field, millify, get_recommendation, ScreenerDataFrame, StockField
from tvscreener.field import Rating, add_rec
from tvscreener.ta import adx


def beautify(df, specific_fields):
    df = Beautify(df, specific_fields).df
    return df


def _percent_colors(row):
    return 'color:red;' if row.startswith("-") < 0 else 'color:green;'


def _rating_colors(row):
    if row.endwiths("B"):
        return 'color:green;'
    elif row.endwiths("S"):
        return 'color:red;'
    else:
        return 'color:gray;'


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
            # TODO
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
            # TODO
            pass
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
            lambda x: f"{x[field.field_name]} - {get_recommendation(x[field.get_rec_field()])}", axis=1)

    def _computed_recommendation(self, field):
        if field.field_name == "ADX":
            # FIXME Column name can have update mode
            self.df[field.field_name] = self.df.apply(
                lambda x: f"{x['ADX']} - {adx(x['ADX'], x['ADX-DI'], x['ADX+DI'], x['ADX-DI[1]'], x['ADX+DI[1]'])}", axis=1)
            self.df_beauty = self.df_beauty.applymap(_rating_colors, subset=pd.IndexSlice[:, [field.field_name]])

    def _number_group(self, field):
        self.df[field.field_name] = self.df[field.field_name].apply(lambda x: millify(x))

    def _percent(self, field):
        self.df[field.field_name] = self.df[field.field_name].apply(lambda x: f"{x:.2f}%" if not np.isnan(x) else "--")
        self.df_beauty = self.df_beauty.applymap(_percent_colors, subset=pd.IndexSlice[:, [field.field_name]])

    def _round(self, field):
        self.df[field.field_name] = self.df[field.field_name].apply(lambda x: round(x, 2) if not np.isnan(x) else "--")

    def _copy_column(self, field):
        raw_name = field.field_name + " raw"
        self.df[raw_name] = self.df[field.field_name]

    def _replace_nan(self, field):
        self.df[field.field_name] = self.df[field.field_name].fillna(0)

    def _to_bool(self, field):
        self.df[field.field_name] = self.df[field.field_name].apply(lambda x: True if x == 'true' else False)
        self.df[field.field_name] = self.df[field.field_name].astype(bool)


