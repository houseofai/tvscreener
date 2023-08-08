from tvscreener import Field, millify, get_recommendation, Rating


def beautify(df, specific_fields):
    df = Beautify(df, specific_fields).df
    return df


class Beautify:
    def __init__(self, df, specific_fields: Field):
        self.df = df.copy()

        for column in self.df.columns:
            # Find the enum with the column name
            specific_field = specific_fields.get_by_label(specific_fields, column)
            if specific_field is not None and specific_field.format is not None:
                # self._copy_column(column)
                # fn = self.fn_mappings.get(format_)
                self._format_column(specific_field, column)

    def _format_column(self, specific_field, column):
        if specific_field.format is 'bool':
            self._to_bool(column)
        elif specific_field.format is 'rating':
            self._rating(column)
        elif specific_field.format is 'round':
            self._round(column)
        elif specific_field.format is 'percent':
            self._percent(column)
        elif specific_field.has_recommendation():
            self._recommendation(column, specific_field)
        elif specific_field.format is 'computed_recommendation':
            # TODO
            pass
        elif specific_field.format is 'text':
            # TODO
            pass
        elif specific_field.format is 'date':
            # TODO
            pass
        elif specific_field.format is 'missing':
            # TODO
            pass
        elif specific_field.format is 'currency':
            # TODO
            pass
        elif specific_field.format is 'float':
            # TODO
            pass
        elif specific_field.format is 'number_group':
            self._replace_nan(column)
            self._number_group(column)
        else:
            print(f"Unknown format: {specific_field.format} for column: {column}")

    def _rating(self, column):
        self.df[column] = self.df[column].apply(lambda x: Rating.find(x).label)

    def _recommendation(self, column, specific_field):
        self.df[column] = self.df.apply(
            lambda x: f"{x[column]} - {get_recommendation(x[specific_field.get_rec_label()])}", axis=1)

    def _number_group(self, column):
        self.df[column] = self.df[column].apply(lambda x: millify(x))

    def _percent(self, column):
        self.df[column] = self.df[column].apply(lambda x: f"{x:.2f}%" if x is not None else None)

    def _round(self, column):
        self.df[column] = self.df[column].apply(lambda x: round(x, 2) if x is not None else None)

    def _copy_column(self, column):
        raw_name = column + " raw"
        self.df[raw_name] = self.df[column]

    def _replace_nan(self, column):
        self.df[column] = self.df[column].fillna(0)

    def _to_bool(self, column):
        self.df[column] = self.df[column].apply(lambda x: True if x is 'true' else False)
        self.df[column] = self.df[column].astype(bool)
