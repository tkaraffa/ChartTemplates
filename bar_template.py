def make_bar_chart(dataframes, names, categories, metrics, segments):
	# shows bar chart visualizations of rate of each category (count) & metric (mean)
	# dataframe: list of dataframes, or list of subset of dataframes
	# names: list of names in string format that correspond to dataframes
	# categories: list of column names in string format with categorical data
	# metrics: list of column names in string format with numeric data
	# segments: list of column names in string format to group by
	import plotly.graph_objects as go
	import pandas as pd

	for segment in segments:
		for metric in metrics:
			fig = go.Figure(layout={'title': metric, 'yaxis_title': 'mean', 'legend_title': segment})
			for name, (df_index, dataframe) in zip(names, enumerate(dataframes)):
				chart_data = dataframe.groupby(segment)[metric].mean()
				chart_data.index = chart_data.index.astype(str)
				for i in chart_data.index.astype(str):
					fig.add_trace(go.Bar(
						x=[''],
						y=[chart_data.loc[i]],
						name=f'{name}: {i}',
						hoverinfo='none',
						text=f'{100 * chart_data.loc[i]:.1f}%',
						textposition='auto'))
			fig.show()
		for category in categories:
			fig = go.Figure(layout={'title': category, 'yaxis_title': 'rate', 'legend_title': segment})
			for name, (df_index, dataframe) in zip(names, enumerate(dataframes)):
				chart_data = dataframe.groupby(segment)[category].value_counts(normalize=True).unstack()
				for i in chart_data.index:
					fig.add_trace(go.Bar(
						x=chart_data.loc[i].index.astype(str),
						y=chart_data.loc[i].values,
						name=f'{name}: {i}',
						hoverinfo='none',
						text=[f'{100 * value:.1f}%' for value in chart_data.loc[i].values],
						textposition='auto'))
			fig.show()

# the comparison of two different dataframes can be done with some fancy subsetting and then appending, using
# the dataframe of origin as the segment, but then using any further segments would treat the appended data as a
# single data source.

# to do: add segments to the following function
def make_bar_chart_mult_sources(dataframes, categories, metrics):
	# shows bar chart visualizations of rate of each category (count) & metric (mean), compared between two different
	# data sets. Can be two slices of the same dataframe.
	# dataframes: list of dataframes to compare
	# categories: list of column names to get value counts
	# segments: list of column names to group by
	import plotly.graph_objects as go
	import pandas as pd

	# create visualizations for each categorical column
	for column in categories:
		fig = go.Figure(layout={'title': f'{column}', 'xaxis_title': column})
		for dataframe in dataframes:
			chart_data = dataframe[column].value_counts(normalize=True)
			chart_data.name = dataframe.name
			fig.add_trace(go.Bar(
				x=chart_data.index.astype(str),
				y=chart_data.values,
				name=chart_data.name,
				hoverinfo='none',
				text=[f'{100 * value:.1f}%' for value in chart_data.values],
				textposition='auto'))
		fig.show()
	# create visualizations for each numerical column
	for column in metrics:
		fig = go.Figure(layout={'title': f'{column}'})
		for dataframe in dataframes:
			chart_data = dataframe[column]
			chart_data.name = dataframe.name
			fig.add_trace(go.Bar(
				x=[''],
				y=[chart_data.mean()],
				name=chart_data.name,
				hoverinfo='none',
				text=f'{100 * chart_data.mean():.1f}%',
				textposition='auto'))
		fig.show()
