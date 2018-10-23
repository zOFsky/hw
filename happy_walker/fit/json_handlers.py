import json
from . import epochtime
def create_json_request(**kwargs):
    my_dict = {}

    for key, value in kwargs.items():
        my_dict[key] = value

    json_string = json.dumps(my_dict)
    return json_string

def get_value_from_json(json_string):
    parsed_json = json.loads(json_string)
    steps_source = "derived:com.google.step_count.delta:com.google.android.gms:aggregated"
    distance_source = "derived:com.google.distance.delta:com.google.android.gms:aggregated"
    calories_source = "derived:com.google.calories.expended:com.google.android.gms:aggregated"
    result_data_list = []

    for elem in parsed_json["bucket"]:
        day_data = {"date":"",
                    "steps":0,
                    "distance":0,
                    "calories":0}
        for dataset_elem in elem["dataset"]:
            milis_time = elem["startTimeMillis"]
            day_data["date"] = epochtime.epoch_to_date(int(milis_time))
            if dataset_elem["dataSourceId"] == steps_source:
                try:
                    day_data["steps"] = dataset_elem["point"][0]["value"][0]["intVal"]
                except (IndexError, KeyError):
                    pass
            elif dataset_elem["dataSourceId"] == distance_source:
                try:
                    day_data["distance"] = dataset_elem["point"][0]["value"][0]["fpVal"]
                except (IndexError, KeyError):
                    pass
            elif dataset_elem["dataSourceId"] == calories_source:
                try:
                    day_data["calories"] = dataset_elem["point"][0]["value"][0]["fpVal"]
                except (IndexError, KeyError):
                    pass
        result_data_list.append(day_data)
    return result_data_list

def get_value_from_json_by_hours(json_string):
    parsed_json = json.loads(json_string)
    steps_source = "derived:com.google.step_count.delta:com.google.android.gms:aggregated"
    distance_source = "derived:com.google.distance.delta:com.google.android.gms:aggregated"
    calories_source = "derived:com.google.calories.expended:com.google.android.gms:aggregated"
    result_data_list = []

    for elem in parsed_json["bucket"]:
        hour_data = {"hour":"",
                    "steps":0,
                    "distance":0,
                    "calories":0}
        for dataset_elem in elem["dataset"]:
            milis_time = elem["startTimeMillis"]
            hour_data["hour"] = epochtime.extract_hour(int(milis_time))
            if dataset_elem["dataSourceId"] == steps_source:
                try:
                    hour_data["steps"] = dataset_elem["point"][0]["value"][0]["intVal"]
                except (IndexError, KeyError):
                    pass
            elif dataset_elem["dataSourceId"] == distance_source:
                try:
                    hour_data["distance"] = dataset_elem["point"][0]["value"][0]["fpVal"]
                except (IndexError, KeyError):
                    pass
            elif dataset_elem["dataSourceId"] == calories_source:
                try:
                    hour_data["calories"] = dataset_elem["point"][0]["value"][0]["fpVal"]
                except (IndexError, KeyError):
                    pass
        if hour_data["steps"] > 0:
            result_data_list.append(hour_data)
    return result_data_list