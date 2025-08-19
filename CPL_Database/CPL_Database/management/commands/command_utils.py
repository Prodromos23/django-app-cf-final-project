

def load_data_from_dataframe_with_mapping(df, model, field_mapping):
    for index, row in df.iterrows():
        model.objects.create(**{field: row[column] for column, field in field_mapping.items()})
        # model.objects.create(using='secondary', **{field: row[column] for column, field in field_mapping.items()})


def load_data_from_dataframe(df, model):
    for index, row in df.iterrows():
        model.objects.create(**row.to_dict())
        # model.objects.create(using='secondary', **row.to_dict())