from typing import Union, List, Dict

import requests
from datetime import MINYEAR, MAXYEAR

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils import timezone
from polymorphic.models import PolymorphicModel

from geo.models import CensusGeography
from indicators.models.viz import DataViz
from indicators.models.time import TimeAxis
from indicators.models.source import CensusSource, CKANSource
from indicators.models.abstract import Described

CKAN_API_BASE_URL = 'https://data.wprdc.org/api/3/'
DATASTORE_SEARCH_SQL_ENDPOINT = 'action/datastore_search_sql'


class Variable(PolymorphicModel, Described):
    units = models.CharField(
        max_length=30,
        null=True,
        blank=True
    )
    unit_notes = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )
    denominators = models.ManyToManyField(
        'Variable',
        help_text='Variables that represent a universe under which the current variable can be analyzed',
        blank=True
    )
    percent_label_text = models.CharField(
        help_text='Label to use when being used as denominator. If not provided, "% of &lt;title&gt;" will be used',
        max_length=100,
        null=True,
        blank=True
    )
    depth = models.IntegerField(
        help_text='Used to represent hierarchy of data. In practice, it is used to indent rows in '
                  'a table corresponding to this variable',
        default=0
    )

    @property
    def percent_label(self):
        return self.percent_label_text if self.percent_label_text else f'% of {self.title}'

    def _get_proportional_datum(self, region: CensusGeography, time_part: TimeAxis.TimePart,
                                denom_variable: "Variable") -> Union[float, None]:
        """ Get or calculate comparison of variable to one of its denominators"""
        # todo: make a `get_value` method to cut out this MoE cruft
        val_and_moe = self.get_value_and_moe(region, time_part)
        denom_val_and_moe = denom_variable.get_value_and_moe(region, time_part)
        if val_and_moe['v'] is None or denom_val_and_moe['v'] in [None, 0]:
            return None
        else:
            return 100 * val_and_moe['v'] / denom_val_and_moe['v']

    def get_proportional_data(self, region: CensusGeography, time_part: TimeAxis.TimePart) -> dict:
        """ Get or calculate comparison of variable to its denominators """
        data = {}
        for denom_variable in self.denominators.all():
            data[denom_variable.slug] = self._get_proportional_datum(region, time_part, denom_variable)

        return data


class CensusVariable(Variable):
    sources = models.ManyToManyField(
        'CensusSource',
        related_name='census_variables',
        through='CensusVariableSource'
    )

    def all_census_tables(self, time_points: [timezone.datetime]):
        return {
            self.get_source_for_time_point(time_point).slug: self.get_formula_parts_at_time_point(time_point)
            for time_point in time_points
        }

    def get_table_row(self, data_viz: DataViz, region: CensusGeography) -> Dict[str, Union[dict, None]]:
        """
        Gets the data for a table row. Data is collected for each series (column) in `data_viz`.
            If denominators are provided, sub rows will also be provided.
        """
        row = {}
        for time_part in data_viz.time_axis.time_parts:
            values = self.get_all_values_at_region_and_time_part(region, time_part)
            if values is not None:
                row[time_part.slug] = values
        return row

    def get_chart_record(self, data_viz: DataViz, region: CensusGeography) -> Dict[str, any]:
        """
        Gets the data for one record displayed in a chart.
            {name: variable.name, [series.name]: f(value, series) }
        """
        record: Dict[str, any] = {'name': self.name}
        for time_part in data_viz.time_axis.time_parts:
            value = self.get_primary_value(region, time_part)
            if value is not None:
                record[time_part.slug] = value
        return record

    def get_primary_value(self, region: CensusGeography, time_part: TimeAxis.TimePart) -> any:
        """  Gets the primary value """
        return self.get_value_and_moe(region, time_part)['v']

    def get_value_and_moe(self, region: CensusGeography, time_part: TimeAxis.TimePart) -> dict:
        """ Find and return the value and margin of error for the variable at a region and series """
        value: float = 0
        moe: float = 0

        source = self.get_source_for_time_point(time_part.time_point)

        for part in self.get_formula_parts_at_time_point(time_part.time_point):
            census_value = self._get_or_create_census_value(part, region, source).value
            if part[-1] == 'M':
                moe += census_value if census_value > 0 else 0  # todo: handle census MOE special values
            else:
                value += census_value
        return {'v': value, 'm': moe}

    def get_all_values_at_region_and_time_part(self, region: CensusGeography, time_part: TimeAxis.TimePart) -> dict:
        """
        Returns a dict that contains the values retrieved with this variable when examined
        in 'region' around (`time_unit`) the point in time 'time_point'

        the keys 'v' and 'm' are value and margin of error respectively.
        all proportional calculations are keyed by their denominator's slug
        {
            series: {v: val, m: margin, d1: p1, d2: p2},
        }
        """
        return {**self.get_value_and_moe(region, time_part),
                **self.get_proportional_data(region, time_part)}

    def get_source_for_time_point(self, time_point: timezone.datetime) -> CensusSource:
        # fixme: come up with a  better solution for this
        is_decade = not time_point.year % 10
        if is_decade:
            return self.sources.filter(dataset='CEN')[0]
        return self.sources.filter(dataset='ACS5')[0]

    def get_formula_parts_at_time_point(self, time_point: timezone.datetime) -> List[str]:
        return self._split_formula(self.get_formula_at_time_point(time_point),
                                   self.get_source_for_time_point(time_point))

    def get_formula_at_time_point(self, time_point: timezone.datetime) -> Union[str, None]:
        formula: Union[str, None] = None
        try:
            source: CensusSource = self.get_source_for_time_point(time_point)
            formula = source.source_to_variable.get(variable=self).formula
        finally:
            return formula

    def _fetch_data_for_region(self, formula_parts: List[str], region: CensusGeography, time_point: timezone.datetime):
        source = self.get_source_for_time_point(time_point)
        return source.get_data(formula_parts, region)

    @staticmethod
    def _split_formula(formula: str, source: CensusSource) -> List[str]:
        """
        Splits up the formula into a list of its table_ids
            for datasets with margins of error, it creates and adds the value and moe table_ids to the list
        """
        result = []
        for part in formula.split('+'):
            if source.dataset == 'CEN':
                result.append(part)
            else:
                result.append(part + 'E')
                result.append(part + 'M')
        return result

    def _extract_values_from_api_response(self, region: CensusGeography, response_data: dict) -> None:
        """
        Take response data and store it into a CensusValue object that is linked to this variable
            and the region provided to the method.
        """
        for part in self.formula_parts:
            if not CensusValue.objects.filter(census_table=part, region=region):
                cv = CensusValue(census_table=part, region=region, value=response_data[self.source][0][part])
                cv.save()

    @staticmethod
    def _get_or_create_census_value(table: str, region: CensusGeography, source: CensusSource):
        try:
            return CensusValue.objects.filter(census_table=table, region=region)[0]  # fixme: should be get
        except (ObjectDoesNotExist, IndexError):
            value: float = source.get_data(table, region)[0][table]
            cv = CensusValue(census_table=table, region=region, value=value)
            cv.save()
            return cv

    def __str__(self):
        return f'{self.slug}'


class CensusVariableSource(models.Model):
    """ for linking Census variables to their sources while keeping track of the census formula format for that combo"""
    variable = models.ForeignKey('CensusVariable', on_delete=models.CASCADE, related_name='variable_to_source')
    source = models.ForeignKey('CensusSource', on_delete=models.CASCADE, related_name='source_to_variable')
    formula = models.TextField()


class CensusValue(models.Model):
    """
    stores a single (region, table, value) tuple
    the the values stored here are a function of the Variable, the Series, and the Geography
    the census table is unique to a Variable-Series combination and is where they're effect comes in
    """
    region = models.ForeignKey('geo.Geography', on_delete=models.CASCADE, db_index=True)
    census_table = models.CharField(max_length=15, db_index=True)  # the census table is a function of the series
    value = models.FloatField(null=True, blank=True)

    class Meta:
        index_together = ('region', 'census_table',)
        unique_together = ('region', 'census_table',)

    def __str__(self):
        return f'{self.census_table}/{self.region} ({self.value})'


class CKANVariable(Variable):
    NONE = 'NONE'
    COUNT = 'COUNT'
    SUM = 'SUM'
    MEAN = 'AVG'
    MODE = 'MODE'
    MAX = 'MAX'
    MIN = 'MIN'
    AGGR_CHOICES = (
        (NONE, 'None'),
        (COUNT, 'Count'),
        (SUM, 'Sum'),
        (MEAN, 'Mean'),
        (MODE, 'Mode'),
        (MAX, 'Maximum'),
        (MIN, 'Minimum'),
    )

    sources = models.ManyToManyField(
        'CKANSource',
        related_name='ckan_variables',
    )

    aggregation_method = models.CharField(
        max_length=5,
        choices=AGGR_CHOICES,
        default=COUNT,
    )

    field = models.CharField(
        help_text='field in source to aggregate',
        max_length=100
    )
    sql_filter = models.TextField(help_text='SQL clause that will be used to filter data.', null=True, blank=True)

    # Data Viz
    def get_table_row(self, data_viz: DataViz, region: CensusGeography) -> Dict[str, Union[dict, None]]:
        """
        Gets the data for a table row. Data is collected for each series (column) in `data_viz`.
            If denominators are provided, sub rows will also be provided.
        """
        row = {}
        for time_frame in data_viz.time_frames.all():
            values = self._get_values_for_region_over_time_frame(region, time_frame)
            if values is not None:
                row[time_frame.slug] = values
        return row

    def get_chart_record(self, data_viz: DataViz, region: CensusGeography) -> Dict[str, any]:
        record: Dict[str, any] = {'name': self.name}
        time_point: timezone.datetime
        for time_frame in data_viz.time_frames.all():
            value = self.get_primary_value(region, time_frame)
            if value is not None:
                record[time_frame.slug] = value
        return record

    def get_primary_value(self, region: CensusGeography, time_part: TimeAxis.TimePart) -> any:
        return self.get_value_and_moe(region, time_part)['v']

    def get_value_and_moe(self, region: CensusGeography, time_part: TimeAxis.TimePart) -> dict:
        value = self._fetch_value_from_ckan(time_part, region)
        return {'v': value, 'm': None}

    def get_all_values_at_region_and_time_part(self, region: CensusGeography, time_part: TimeAxis.TimePart) -> dict:
        """
        Returns a dict that contains the values retrieved with this variable when examined
        in 'region' across the series in 'series'

        the keys 'v' and 'm' are value and margin of error respectively.
        all proportional calculations are keyed by their denominator's slug
        {
            series: {v: val, m: margin, d1: p1, d2: p2},
        }
        """
        return self.get_value_and_moe(region, time_part)

    def _get_source_for_time_point(self, time_point: timezone.datetime) -> CKANSource:
        """ Return CKAN source that covers the time in `time_point` """
        # fixme: we'll need to come up with a more correct way of doing this: maybe a `through` relationship
        source: CKANSource
        for source in self.sources.all():
            # go through the sources and get the first one who's range covers the point
            start = source.time_coverage_start if source.time_coverage_start else timezone.datetime(MINYEAR, 1, 1)
            end = source.time_coverage_end if source.time_coverage_end else timezone.datetime(MAXYEAR, 1, 1)
            if start < time_point < end:
                return source
        return self.sources.all()[0]  # hack cop-out for now to keep this functions type

    # TODO: make this a function and put it in utils or something
    @staticmethod
    def _query_datastore(query: str):
        url = CKAN_API_BASE_URL + DATASTORE_SEARCH_SQL_ENDPOINT
        r = requests.post(
            url,
            json={'sql': query},
            headers={
                'Cache-Control': 'no-cache'
            }
        )
        response = r.json()
        data = response['result']['records']
        value = data[0]['v']
        return value

    def _fetch_value_from_ckan(self, time_part: TimeAxis.TimePart, region: CensusGeography):
        """
        Query CKAN for some aggregation of this variable within its region.
        (e.g. mean housing sale price in Bloomfield)
        """
        join_statement = ''  # todo if necessary

        aggregation_method = self.aggregation_method if self.aggregation_method != 'NONE' else ''
        target_field = self.field if self.field in ('*',) else f'"{self.field}"'
        source = self._get_source_for_time_point(time_part.time_point)

        cast = '::int' if aggregation_method in ('COUNT',) else ''

        geom_filter_clause = source.get_geom_filter_sql(region)
        time_filter_clause = source.get_time_filter_sql(time_part)

        # generate sql query to send to `/datastore_search_sql` endpoint
        # noinspection SqlResolve
        query = f"""
        SELECT {aggregation_method}({target_field}){cast} as "v", {source.std_time_sql_identifier}
        FROM {f'({join_statement}) as sub_query' if join_statement else f'"{source.resource_id}"'}
        WHERE  {f'{self.sql_filter} AND' if self.sql_filter else ''}
            {geom_filter_clause} AND {time_filter_clause}
        """
        return self._query_datastore(query)
