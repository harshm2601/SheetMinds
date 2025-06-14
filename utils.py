def get_file_extension(filename):
    return filename.split('.')[-1].lower()

def get_data_overview(df, sample_rows=5):
    schema = str(df.dtypes)
    sample = df.head(sample_rows).to_dict()
    return schema, sample
