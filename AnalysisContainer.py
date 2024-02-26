import ExperimentViews as ev
import StatsContainer as st
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

def outlier_analysis(views : ev.ExperimentViews, plot = True):
	print('Calculating outliers...')
	independent_variables = ['fix_mean', 'fix_duration_trial_mean', 'elapsed_time_mean']
	print('The following independent variables were considered: ', end="")
	print(independent_variables)

	remove_list = []
	exp_types_local = views.exp_types
	exp_types_local.reverse()

	for var in independent_variables:
		var_view_list = []
		for exp_type in exp_types_local:
			exp_group = views.df_participant_view[views.df_participant_view['exp_type'] == exp_type]
			outliers_idx = st.outlier_iqr(exp_group[var])
			# Remove outliers from data
			remove_list.extend([exp_group['num_id'].loc[x] for x in outliers_idx]) # here is 'loc' (original index)
			var_view_list.append(exp_group[var])
		if plot:
			# Plot box-plot (before)
			plt.figure()
			plt.boxplot(var_view_list, labels = exp_types_local)
			plt.title("Box Plot with Outliers")
			plt.ylabel(var)
			plt.xlabel('Experiment Type')
			plt.show(block=False)
			plt.pause(0.01)
			plt.tight_layout()
			fileName = r'Export\Figures\Figure_'+str(plt.gcf().number)
			plt.savefig(fileName+'.png')
			plt.savefig(fileName+'.svg')

	# Remove outliers from data
	remove_list = list(set(remove_list)) # remove duplicates
	remove_list.sort()
	print('The following participants were removed (num_id): ', end="")
	print(remove_list)
	
	# Propagate removal to all views & experiment
	views.remove_participants(remove_list)

	# Plot box-plot (after)
	for var in independent_variables:
		var_view_list = []
		for exp_type in exp_types_local:
			exp_group = views.df_participant_view[views.df_participant_view['exp_type'] == exp_type]
			var_view_list.append(exp_group[var])
		if plot:
			plt.figure()
			plt.boxplot(var_view_list, labels = exp_types_local)
			plt.title('Box Plot without Outliers (IQR)')
			plt.ylabel(var)
			plt.xlabel('Experiment Type')
			plt.show(block=False)
			plt.pause(0.01)
			plt.tight_layout()
			fileName = r'Export\Figures\Figure_'+str(plt.gcf().number)
			plt.savefig(fileName+'.png')
			plt.savefig(fileName+'.svg')

	# Plot box-plot Accuracy
	var_view_list = []
	for exp_type in exp_types_local:
		exp_group = views.df_participant_view[views.df_participant_view['exp_type'] == exp_type]
		var_view_list.append(exp_group['accuracy'])
	if plot:
		plt.figure()
		plt.boxplot(var_view_list, labels = exp_types_local)
		plt.title('Box Plot')
		plt.ylabel('Accuracy')
		plt.xlabel('Experiment Type')
		plt.show(block=False)
		plt.pause(0.01)
		plt.tight_layout()
		fileName = r'Export\Figures\Figure_'+str(plt.gcf().number)
		plt.savefig(fileName+'.png')
		plt.savefig(fileName+'.svg')


def confusion_analysis(views : ev.ExperimentViews):
	exp_types_local = views.exp_types
	expressions = views.expressions

	for exp_type in exp_types_local:
		exp_group = views.df_trial_view[views.df_trial_view['exp_type'] == exp_type]
		cm = confusion_matrix(exp_group['expression'], exp_group['answer_q1'], labels = expressions, normalize='true')
		disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels = expressions)
		disp.plot()
		#plt.title('Experiment Type: '+exp_type+'; n='+str(len(exp_group['num_id'].unique()))+'; trials='+str(len(exp_group[exp_group['num_id']==exp_group['num_id'].iloc[0]])))
		plt.title(exp_type)
		plt.show(block=False)
		plt.pause(0.01)
		plt.tight_layout()
		fileName = r'Export\Figures\Figure_'+str(plt.gcf().number)
		plt.savefig(fileName+'.png', dpi = 300)
		plt.savefig(fileName+'.svg')


def confusion_analysis_by_gender(views : ev.ExperimentViews):
	exp_types_local = views.exp_types
	expressions = views.expressions
	gender = ['M', 'F']

	for exp_type in exp_types_local:
		for g in gender:
			exp_group = views.df_trial_view[views.df_trial_view['exp_type'] == exp_type]
			exp_group = exp_group[exp_group['gender'] == g]
			cm = confusion_matrix(exp_group['expression'], exp_group['answer_q1'], labels = expressions, normalize='true')
			disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels = expressions)
			disp.plot()
			plt.title('Experiment Type: '+exp_type+'; facial gender='+g+' n='+str(len(exp_group['num_id'].unique()))+'; trials='+str(len(exp_group[exp_group['num_id']==exp_group['num_id'].iloc[0]])))
			plt.show(block=False)
			plt.pause(0.01)
			plt.tight_layout()
			fileName = r'Export\Figures\Figure_'+str(plt.gcf().number)
			plt.savefig(fileName+'.png', dpi = 300)
			plt.savefig(fileName+'.svg')


def violin_plot_by_exp_condition(views : ev.ExperimentViews):
	measures = ['accuracy', 'elapsed_time_mean', 'fix_mean', 'fix_duration_mean']
	labels = ['Accuracy', 'Inspection Time', 'Number of Fixations', 'Fixation Duration']
	labels_axis = ['Accuracy (%)', 'Time (s)', 'Number', 'Time (ms)']

	exp_group = views.df_participant_view.copy()
	exp_group["exp_type"] = pd.Categorical(exp_group["exp_type"], categories=['NVR', 'PFFV', 'FV'], ordered=True)

	#plt.figure()
	fig, axs = plt.subplots(2, 2, figsize=(12, 9))

	for i, ax in enumerate(axs.flat):
		sns.violinplot(data=exp_group, x='exp_type', y=measures[i], inner_kws=dict(box_width=8, whis_width=2), ax=ax) # cut = 0
		ylim = ax.get_ylim()
		ax.set_ylim(ylim[0], ylim[1] * 1.15)
		ax.set_title(labels[i])
		ax.set_xlabel('') # Experimental Condition (implicit) 
		ax.set_ylabel(labels_axis[i])
	plt.show(block=False)
	plt.pause(0.01)
	plt.tight_layout()
	fileName = r'Export\Figures\Figure_'+str(plt.gcf().number)
	plt.savefig(fileName+'.png', dpi = 300)
	plt.savefig(fileName+'.svg')


def violin_plot_by_gender(views : ev.ExperimentViews):
	measures = ['accuracy', 'elapsed_time_mean', 'fix_mean', 'fix_duration_mean']
	labels = ['Accuracy', 'Inspection Time', 'Number of Fixations', 'Fixation Duration']
	labels_axis = ['Accuracy (%)', 'Time (s)', 'Number', 'Time (ms)']

	# Adjusting DataFrames to merge M/F columns
	m_exp_group = views.df_participant_view[['exp_type','M_acc', 'M_elapsed_time_mean', 'M_fix_mean', 'M_fix_duration_mean']].copy()
	f_exp_group = views.df_participant_view[['exp_type','F_acc', 'F_elapsed_time_mean', 'F_fix_mean', 'F_fix_duration_mean']].copy()
	m_exp_group['Facial Gender'] = 'M'
	f_exp_group['Facial Gender'] = 'F'
	m_exp_group.rename(columns={'M_acc': 'accuracy'}, inplace=True)
	f_exp_group.rename(columns={'F_acc': 'accuracy'}, inplace=True)
	m_exp_group.rename(columns={'M_elapsed_time_mean': 'elapsed_time_mean'}, inplace=True)
	f_exp_group.rename(columns={'F_elapsed_time_mean': 'elapsed_time_mean'}, inplace=True)
	m_exp_group.rename(columns={'M_fix_mean': 'fix_mean'}, inplace=True)
	f_exp_group.rename(columns={'F_fix_mean': 'fix_mean'}, inplace=True)
	m_exp_group.rename(columns={'M_fix_duration_mean': 'fix_duration_mean'}, inplace=True)
	f_exp_group.rename(columns={'F_fix_duration_mean': 'fix_duration_mean'}, inplace=True)

	concat_exp_group = pd.concat([m_exp_group, f_exp_group])
	concat_exp_group["exp_type"] = pd.Categorical(concat_exp_group["exp_type"], categories=['NVR', 'PFFV', 'FV'], ordered=True)

	#plt.figure()
	fig, axs = plt.subplots(2, 2, figsize=(12, 9))

	for i, ax in enumerate(axs.flat):
		sns.violinplot(data=concat_exp_group, x="exp_type", y=measures[i], hue="Facial Gender", split=True, gap=.1, inner="quart", inner_kws=dict(linewidth=2.5), ax=ax)
		ax.legend(loc='lower right') # supress legend title
		ylim = ax.get_ylim()
		ax.set_ylim(ylim[0], ylim[1] * 1.2)
		ax.set_title(labels[i])
		ax.set_xlabel('') # Experimental Condition (implicit) 
		ax.set_ylabel(labels_axis[i])
	plt.show(block=False)
	plt.pause(0.01)
	plt.tight_layout()
	fileName = r'Export\Figures\Figure_'+str(plt.gcf().number)
	plt.savefig(fileName+'.png', dpi = 300)
	plt.savefig(fileName+'.svg')


def dealocate_analysis_objects():
	print('Close all figures to proceed...')
	plt.show(block=True) # Deals with block = False (otherwise figures become unresponsive)
	plt.close('all')