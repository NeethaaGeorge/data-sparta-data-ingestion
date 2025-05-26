import pandas as pd
import dlt
import os

@dlt.resource(name="neetha_source")
def read_api():
    # This is where your code goes. 
    # You need to read from API and return pandas dataframe
    # df = pd.DataFrame({
    #     "id": [1, 2, 3],
    #     "name": ["Bulbasaur", "Ivysaur", "Venusaur"],
    #     "height": [7, 10, 13],
    #     "weight": [69, 130, 100]
    # })
    csv_path = os.path.join(os.path.dirname(__file__), 'weather_hourly_AUS_last_6_days.csv')
    df = pd.read_csv(csv_path)
    yield df


def load_github() -> None:
    pipeline = dlt.pipeline(
        pipeline_name="neetha_pipeline",
        destination='athena',
        dataset_name="neetha",
    )

    load_info = pipeline.run(read_api())
    print(load_info)

if __name__ == "__main__":
        load_github()