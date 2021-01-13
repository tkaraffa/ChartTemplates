def make_time_series(dataframes, date_column, metrics, aggregates):
    # takes a list of dataframes (or subsets of the same dataframe) and returns a time series with useful
    # descriptive statistics

    # dataframes: list of NAMED dataframes, or list of NAMED subsets of dataframes
    # date_column: string representation of date column
    # metrics: numerical data
    # aggregates: list of len>=1 of aggregations. First is graphed; optional remainder are hover labels
    import pandas as pd
    import numpy as np
    import plotly.graph_objects as go
    main_agg, sub_aggs = aggregates.pop(0), [*aggregates]
    for metric in metrics:
        fig = go.Figure(layout={
            'title': metric.replace('_', ' ').title(),
            'yaxis_title': main_agg})
        for dataframe in dataframes:
            grouped_df = dataframe.groupby(date_column)[metric]
            time_data = grouped_df.agg(main_agg)
            time_data.index = pd.to_datetime(time_data.index, format='%Y%m')

            # gratuitous formatting for dynamic hover text

            customdata_text = ''  # initialize, will be overwritten if any sub aggregates
            customdata = []  # initialize, will be overwritten if any sub aggregates
            if sub_aggs:
                # aggregate the groupby by each sub_aggregation, then insert that value into a formatted string,
                # to later use in the "customdata" attribute of the figre
                customdata = np.stack([grouped_df.agg(sub_agg).values for sub_agg in sub_aggs], axis=-1)
                customdata_text = ''.join([f"{sub_agg.title()}: %{{customdata[{i}]:.2f}}<br>"
                                           for sub_agg, (i, data) in zip(sub_aggs, enumerate(customdata))])

            fig.add_trace(go.Scatter(
                x=time_data.index.astype(str),
                y=time_data.values,
                name=dataframe.name,
                ### optional data labels
                # mode="lines+markers+text",
                # text=time_data.values.astype(str),
                # textposition='top center'
                customdata=customdata,
                hovertemplate=
                "%{x}<br>" +
                f"{main_agg.title()}: %{{y}}<br>" +
                customdata_text +
                "<extra></extra>",
            ))
        fig.show()
