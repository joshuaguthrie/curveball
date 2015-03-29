import matplotlib.pyplot as plt
import seaborn as sns

def plot_96wells(df, x, y, func=plt.plot, output_filename=None):
	if 'Strain' in df:
		hue = 'Strain'
	else:
		hue = 'Well'
	g = sns.FacetGrid(df, hue=hue, col='Number', row='Letter', 
                  sharex=True, sharey=True, size=1,
                  aspect=12./8., despine=True,margin_titles=True)
	g.map(func, x, y)
	g.fig.set_figwidth(12) 
	g.fig.set_figheight(8)
	plt.locator_params(nbins=4) # 4 ticks is enough
	g.set_axis_labels('','') # remove facets axis labels
	g.fig.text(0.5, 0, x, size='x-large') # xlabel
	g.fig.text(-0.01, 0.5, y, size='x-large', rotation='vertical') # ylabel
	if output_filename:
		g.savefig(output_filename, bbox_inches='tight', pad_inches=1)
	return g
