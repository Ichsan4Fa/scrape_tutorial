import pandas as pd

def transform_to_dataframe(data):
    df = pd.DataFrame(data)
    return df

def transform_csv_to_dataframe(file_path):
    df = pd.read_csv(file_path)
    return df

def transform_data(data,exchange_rate):
    # Price is in format "£51.77"
    data["Price_in_pounds"] = data["Price"].apply(lambda x: float(x.replace("£", "")))

    # Rate transformation
    rating_mapping = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }
    data["Rating"] = data["Rating"].map(rating_mapping)

    # Exchange rate transformation
    data["Price_in_rupiah"] = (data["Price_in_pounds"] * exchange_rate).astype(int)

    # Redudant columns
    data.drop(columns=["Price", "Price_in_pounds"], inplace=True)

    # Data type transformation
    data['Title'] = data['Title'].astype('string')
    data["Availability"] = data["Availability"].astype('string')

    return data