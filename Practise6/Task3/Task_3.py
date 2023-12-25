import pandas as pd
import os
import json

pd.set_option("display.max_rows", 20, "display.max_columns", 60)


def read_file(file_name):
    return pd.read_csv(file_name)


def get_memory_stat_by_column(df):
    memory_update_stat = df.memory_usage(deep=True)
    total_memory_usage = memory_update_stat.sum()
    print(f'file in memory size   = {total_memory_usage // 1024:10} КБ')

    column_stat = []
    for key in df.dtypes.keys():
        column_stat.append({'column_name': key,
                            'memory_abs': int(memory_update_stat[key] // 1024),
                            "memory_per": float(round(memory_update_stat[key] / total_memory_usage * 100, 4)),
                            'dtype': str(df.dtypes[key])})
    column_stat.sort(key=lambda x: x['memory_abs'], reverse=True)
    return column_stat



def mem_usage(pandas_obj):
    if isinstance(pandas_obj, pd.DataFrame):
        usage_b = pandas_obj.memory_usage(deep=True).sum()
    else:
        usage_b = pandas_obj.memory_usage(deep=True)
    usage_mb = usage_b / 1024 ** 2
    return "{:03.2f} MB".format(usage_mb)


def opt_obj(df):
    converted_obj = pd.DataFrame()
    dataset_obj = df.select_dtypes(include=['object']).copy()

    for col in dataset_obj.columns:
        num_unique_values = len(dataset_obj[col].unique())
        num_total_values = len(dataset_obj[col])
        if num_unique_values / num_total_values < 0.5:
            converted_obj.loc[:, col] = dataset_obj[col].astype('category')
        else:
            converted_obj.loc[:, col] = dataset_obj[col]

    print(mem_usage(dataset_obj))
    print(mem_usage(converted_obj))
    return converted_obj


def opt_int(df):
    data_int = df.select_dtypes(include=['int'])

    converted_int = data_int.apply(pd.to_numeric, downcast='unsigned')
    print(mem_usage(data_int))
    print(mem_usage(converted_int))

    compare_ints = pd.concat([data_int.dtypes, converted_int.dtypes], axis=1)
    compare_ints.columns = ['before', 'after']
    compare_ints.apply(pd.Series.value_counts)
    print(compare_ints)

    return converted_int


def opt_float(df):
    data_float = df.select_dtypes(include=['float'])

    converted_float = data_float.apply(pd.to_numeric, downcast='float')
    print(mem_usage(data_float))
    print(mem_usage(converted_float))

    compare_floats = pd.concat([data_float.dtypes, converted_float.dtypes], axis=1)
    compare_floats.columns = ['before', 'after']
    compare_floats.apply(pd.Series.value_counts)
    print(compare_floats)

    return converted_float

file_name = "[3]flights.csv"
data = read_file(file_name)
file_size = os.path.getsize(file_name)
print(f'file size             = {file_size // 1024:10} КБ')

get_memory_stat_by_column(data)
with open("get_memory_stat_by_column.json", 'w',  encoding="utf-8") as f:
    f.write(json.dumps(get_memory_stat_by_column(data), ensure_ascii=False))


optimized_data = data.copy()

converted_obj = opt_obj(data)
converted_int = opt_int(data)
converted_float = opt_float(data)


optimized_data[converted_obj.columns] = converted_obj
optimized_data[converted_int.columns] = converted_int
optimized_data[converted_float.columns] = converted_float

print(mem_usage(data))
print(mem_usage(optimized_data))
get_memory_stat_by_column(optimized_data)
with open("get_memory_stat_by_column_optimized.json", 'w',  encoding="utf-8") as f:
    f.write(json.dumps(get_memory_stat_by_column(optimized_data), ensure_ascii=False))



need_column = dict()
column_names = ['CANCELLED', 'AIRLINE',
                'TAIL_NUMBER', 'LATE_AIRCRAFT_DELAY',
                'TAXI_IN','ORIGIN_AIRPORT',
                'DEPARTURE_TIME', 'SCHEDULED_DEPARTURE',
                'FLIGHT_NUMBER','DAY_OF_WEEK']
opt_dtypes = optimized_data.dtypes
for key in column_names:
    need_column[key] = opt_dtypes[key]
    print(f'{key}:{opt_dtypes[key]}')


with open("dtypes.json", mode='w') as file:
    dtypes_json = need_column.copy()
    for key in dtypes_json.keys():
        dtypes_json[key] = str(dtypes_json[key])

    json.dump(dtypes_json, file)

read_and_optimized = pd.read_csv(file_name,
                                 usecols=lambda x: x in column_names,
                                 dtype=need_column,
                                 )

print(read_and_optimized.shape)
print(mem_usage(read_and_optimized))

has_header = True
for chunk in pd.read_csv(file_name,
                         usecols=lambda x: x in column_names,
                         dtype=need_column,
                         # parse_dates=['date'],
                         # infer_datetime_format=True,
                         chunksize=100_000):
    print(mem_usage(chunk))
    chunk.to_csv("df.csv", mode='a', header=has_header)
    has_header = False