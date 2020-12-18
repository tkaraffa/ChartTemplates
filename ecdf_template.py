def make_cdf_chart(df):
    # takes dataframe, outputs cumulative distribution formula chart of numeric data with points of note marked
    import numpy as np
    from statsmodels.distributions.empirical_distribution import ECDF
    import plotly.graph_objects as go
    import plotly
    palette = plotly.colors.qualitative.Dark24

    metrics = list(df.select_dtypes(include='number'))
    colors = palette[:len(metrics)]  # get colors from the Dark24 palette to match metrics
    fig = go.Figure(layout={'title': f"CDF: {', '.join(metrics)}"})  # initialize figure with title

    for metric, color in zip(metrics, colors):  # add a cdf line for each provided metric
        fig.add_trace(go.Scatter(x=np.unique(df[metric]),
                                 y=ECDF(df[metric])(np.unique(df[metric])),
                                 line_shape='linear',
                                 name=metric,
                                 visible=True,
                                 line={'color': color},
                                 hoverinfo='none',
                                 legendgroup=metric))

        minimum, q1, med, q3, maximum = df[metric].quantile([0, .25, .5, .75, 1])  # calculate quantile values
        points = [[minimum, 0, 'Minimum'],  # get data to use for points
                  [q1, .25, 'Q1'],
                  [med, .5, 'Median'],
                  [q3, .75, 'Q3'],
                  [maximum, 1, 'Maximum']]

        for point in points:  # add points to figure
            fig.add_trace(go.Scatter(
                hoverinfo='text',
                line={'color': color},
                x=[point[0]],
                y=[point[1]],
                mode="markers",
                showlegend=False,
                marker={'size': 9},
                hovertext=f'<b>{metric}</b> {point[2]}: {point[0]}',
                opacity=.5,
                visible=bool(fig.data[0].visible),
                legendgroup=metric
            ))

    lines = {'Q1': .25, 'Median': .5, 'Q3': .75}
    for q, n in lines.items():  # add a line to the cdf graph to mark Q1, Median, and Q3
        fig.add_trace(go.Scatter(mode='lines+text',
                                 x=[0, df[metrics].values.max()],
                                 y=[n, n],
                                 showlegend=False,
                                 line={'color': 'gray', 'width': 1},
                                 text=[q, q],
                                 textposition=['middle left', 'middle right']))
    fig.show()