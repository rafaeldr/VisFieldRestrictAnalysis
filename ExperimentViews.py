import pandas as pd

class ExperimentViews:

	def __init__(self, experiment, exp_types, expressions):
		self.experiment = experiment		# list of ParticipantResults objects
		self.expressions = expressions		
		self.exp_types = exp_types
		self.df_trial_view = None			# later assigned
		self.df_participant_view = None		# later assigned

	def generate_trial_view(self, export = True):
		print('Generating experiment trial view...')
		results_df = pd.DataFrame() # hold the results

		for participant in self.experiment:
			participant_data = participant.experiment_data
			id_col = [participant.num_id] * len(participant_data)
			exp_type_col = [participant.exp_type] * len(participant_data)
			df_temp = participant_data.copy() # shallow copy
			df_temp.insert(loc=0, column='exp_type', value=exp_type_col)
			df_temp.insert(loc=0, column='num_id', value=id_col)
			# Fixations Descriptve Statistics
			fixations_list = participant.fixations_data
			total_fixations = []
			x_min, x_max, x_mean = [], [], []
			y_min, y_max, y_mean = [], [], []
			duration_total, duration_min, duration_max, duration_mean, duration_std = [], [], [], [], []
			gaze_points_total, gaze_points_min, gaze_points_max, gaze_points_mean, gaze_points_std = [], [], [], [], []
			for fixations in fixations_list:
				total_fixations.append(len(fixations))
				dt_fixations = pd.DataFrame(fixations, columns=['X_coord', 'Y_coord', 'Duration', 'Start_time', 'End_time', 'No_gaze_points'])
				x_min.append(dt_fixations['X_coord'].min())
				x_max.append(dt_fixations['X_coord'].max())
				x_mean.append(dt_fixations['X_coord'].mean())
				y_min.append(dt_fixations['Y_coord'].min())
				y_max.append(dt_fixations['Y_coord'].max())
				y_mean.append(dt_fixations['Y_coord'].mean())
				duration_total.append(sum(dt_fixations['Duration']))
				duration_min.append(dt_fixations['Duration'].min())
				duration_max.append(dt_fixations['Duration'].max())
				duration_mean.append(dt_fixations['Duration'].mean())
				duration_std.append(dt_fixations['Duration'].std())
				gaze_points_total.append(sum(dt_fixations['No_gaze_points']))
				gaze_points_min.append(dt_fixations['No_gaze_points'].min())
				gaze_points_max.append(dt_fixations['No_gaze_points'].max())
				gaze_points_mean.append(dt_fixations['No_gaze_points'].mean())
				gaze_points_std.append(dt_fixations['No_gaze_points'].std())
			df_temp['fixations'] = total_fixations
			df_temp['x_min'], df_temp['x_max'], df_temp['x_mean'] = x_min, x_max, x_mean
			df_temp['y_min'], df_temp['y_max'], df_temp['y_mean'] = y_min, y_max, y_mean
			df_temp['fix_duration_total'], df_temp['fix_duration_min'], df_temp['fix_duration_max'], df_temp['fix_duration_mean'], df_temp['fix_duration_std'] = duration_total, duration_min, duration_max, duration_mean, duration_std
			df_temp['gaze_points_total'], df_temp['gaze_points_min'], df_temp['gaze_points_max'], df_temp['gaze_points_mean'], df_temp['gaze_points_std'] = gaze_points_total, gaze_points_min, gaze_points_max, gaze_points_mean, gaze_points_std
			calibration_col = [participant.calibration] * len(participant_data)
			df_temp['calibration'] =calibration_col
			# Concatenate the new dataframe with the results dataframe
			results_df = pd.concat([results_df, df_temp], ignore_index=True)
	
		results_df.reset_index(inplace=True, drop=True) # adjust indexing
		if export:
			results_df.to_excel(r'Export\view_trial.xlsx')
		self.df_trial_view = results_df

	def export_trial_view(self):
		if self.df_trial_view is not None:
			self.df_trial_view.to_excel(r'Export\view_trial.xlsx')

	def import_trial_view(self):
		try:
			self.df_trial_view = pd.read_excel(r"DataSource\view_trial.xlsx")
		except:
			print('Unexpected error: Import file view_trial.xlsx not found in DataSource directory.')
			exit(1)

	def generate_participant_view(self, export = True):
		print('Generating experiment participant view...')
		results_df = pd.DataFrame() # hold the results
		d_rows = dict()

		for participant in self.experiment:
			participant_data = participant.experiment_data

			# Basic information
			d_rows.setdefault('num_id', []).append(participant.num_id)
			d_rows.setdefault('exp_type', []).append(participant.exp_type)

			# Correct answers
			value = sum(participant_data['ans_match']) # correct answers
			d_rows.setdefault('correct', []).append(value)
			value = participant_data['ans_match'].mean() # accuracy
			d_rows.setdefault('accuracy', []).append(value)
			value = participant_data['answer_q2_numeric'].mean() # mean "confidence"
			d_rows.setdefault('confidence', []).append(value)

			# Elapsed time
			view = participant_data['elapsed_time']
			value = sum(view) # total time
			d_rows.setdefault('elapsed_time_total', []).append(value)
			value = view.mean() # mean time
			d_rows.setdefault('elapsed_time_mean', []).append(value)
			value = view.std() # std time
			d_rows.setdefault('elapsed_time_std', []).append(value)

			# Fixations
			fixations_list = participant.fixations_data
			# Loop for each trial
			fix_rows = dict() # used only inside the loop
			for fixations in fixations_list:
				df_fixations_trial = pd.DataFrame(fixations, columns=['X_coord', 'Y_coord', 'Duration', 'Start_time', 'End_time', 'No_gaze_points'])
				value = len(fixations) # total fixations
				fix_rows.setdefault('fix_total', []).append(value)
				value = sum(df_fixations_trial['Duration']) # total duration
				fix_rows.setdefault('fix_duration_total', []).append(value)
				value = sum(df_fixations_trial['No_gaze_points']) # total gaze points
				fix_rows.setdefault('fix_gazep_total', []).append(value)
			df_trial_fixations_summary = pd.DataFrame.from_dict(fix_rows)
			# fixations quantity
			view = df_trial_fixations_summary['fix_total']
			value = sum(view) # total fixations
			d_rows.setdefault('fix_total', []).append(value)
			value = view.mean() # mean fixations
			d_rows.setdefault('fix_mean', []).append(value)
			value = view.std() # std fixations
			d_rows.setdefault('fix_std', []).append(value)
			# fixations duration (by fixation)
			view = df_trial_fixations_summary['fix_duration_total'] / df_trial_fixations_summary['fix_total']
			value = view.mean() # mean duration
			d_rows.setdefault('fix_duration_mean', []).append(value)
			value = view.std() # std duration
			d_rows.setdefault('fix_duration_std', []).append(value)
			# fixations duration grouped by trial
			view = df_trial_fixations_summary['fix_duration_total']
			value = sum(view) # total duration
			d_rows.setdefault('fix_duration_trial_sum', []).append(value)
			value = view.mean() # mean duration
			d_rows.setdefault('fix_duration_trial_mean', []).append(value)
			value = view.std() # std duration
			d_rows.setdefault('fix_duration_trial_std', []).append(value)
			# gaze points (by fixation)
			view = df_trial_fixations_summary['fix_gazep_total'] / df_trial_fixations_summary['fix_total']
			value = view.mean() # mean gaze points
			d_rows.setdefault('fix_gazep_mean', []).append(value)
			value = view.std() # std gaze points
			d_rows.setdefault('fix_gazep_std', []).append(value)
			# gaze points grouped by trial
			view = df_trial_fixations_summary['fix_gazep_total']
			value = sum(view) # total gaze points
			d_rows.setdefault('fix_gazep_trial_sum', []).append(value)
			value = view.mean() # mean gaze points
			d_rows.setdefault('fix_gazep_trial_mean', []).append(value)
			value = view.std() # std gaze points
			d_rows.setdefault('fix_gazep_trial_std', []).append(value)

			# By Face gender
			gender = ['M','F']
			for g in gender:
				# answers
				view = participant_data[participant_data['gender']==g]
				idx_gender = view.index.to_list()
				value = sum(view['ans_match']) # Male/Female: correct answers
				d_rows.setdefault(g+'_correct', []).append(value)
				value = view['ans_match'].mean() # Male/Female: accuracy
				d_rows.setdefault(g+'_acc', []).append(value)
				value = view['answer_q2_numeric'].mean() # Male/Female: confidence
				d_rows.setdefault(g+'_conf', []).append(value)
				# elapsed time
				view = participant_data[participant_data['gender']==g]['elapsed_time']
				value = sum(view)
				d_rows.setdefault(g+'_elapsed_time_total', []).append(value)
				value = view.mean()
				d_rows.setdefault(g+'_elapsed_time_mean', []).append(value)
				value = view.std()
				d_rows.setdefault(g+'_elapsed_time_std', []).append(value)
				# FIXATIONS
				# fixations quantity
				view = df_trial_fixations_summary.iloc[idx_gender]['fix_total']
				value = sum(view) # total fixations
				d_rows.setdefault(g+'_fix_total', []).append(value)
				value = view.mean() # mean fixations
				d_rows.setdefault(g+'_fix_mean', []).append(value)
				value = view.std() # std fixations
				d_rows.setdefault(g+'_fix_std', []).append(value)
				# fixations duration (by fixation)
				view = df_trial_fixations_summary.iloc[idx_gender]['fix_duration_total'] / df_trial_fixations_summary.iloc[idx_gender]['fix_total']
				value = view.mean() # mean duration
				d_rows.setdefault(g+'_fix_duration_mean', []).append(value)
				value = view.std() # std duration
				d_rows.setdefault(g+'_fix_duration_std', []).append(value)
				# fixations duration grouped by trial
				view = df_trial_fixations_summary.iloc[idx_gender]['fix_duration_total']
				value = sum(view) # total duration
				d_rows.setdefault(g+'_fix_duration_trial_sum', []).append(value)
				value = view.mean() # mean duration
				d_rows.setdefault(g+'_fix_duration_trial_mean', []).append(value)
				value = view.std() # std duration
				d_rows.setdefault(g+'_fix_duration_trial_std', []).append(value)
				# gaze points (by fixation)
				view = df_trial_fixations_summary.iloc[idx_gender]['fix_gazep_total'] / df_trial_fixations_summary.iloc[idx_gender]['fix_total']
				value = view.mean() # mean gaze points
				d_rows.setdefault(g+'_fix_gazep_mean', []).append(value)
				value = view.std() # std gaze points
				d_rows.setdefault(g+'_fix_gazep_std', []).append(value)
				# gaze points grouped by trial
				view = df_trial_fixations_summary.iloc[idx_gender]['fix_gazep_total']
				value = sum(view) # total gaze points
				d_rows.setdefault(g+'_fix_gazep_trial_sum', []).append(value)
				value = view.mean() # mean gaze points
				d_rows.setdefault(g+'_fix_gazep_trial_mean', []).append(value)
				value = view.std() # std gaze points
				d_rows.setdefault(g+'_fix_gazep_trial_std', []).append(value)

			# By Face expression
			for exp in self.expressions:
				# answers
				view = participant_data[participant_data['expression']==exp]
				idx_exp = view.index.to_list()
				value = sum(view['ans_match']) # correct answers
				d_rows.setdefault(exp+'_correct', []).append(value)
				value = view['ans_match'].mean() # accuracy
				d_rows.setdefault(exp+'_acc', []).append(value)
				value = view['answer_q2_numeric'].mean() # mean "confidence"
				d_rows.setdefault(exp+'_conf', []).append(value)
				# elapsed time
				view = participant_data[participant_data['expression']==exp]['elapsed_time']
				value = sum(view)
				d_rows.setdefault(exp+'_elapsed_time_total', []).append(value)
				value = view.mean()
				d_rows.setdefault(exp+'_elapsed_time_mean', []).append(value)
				value = view.std()
				d_rows.setdefault(exp+'_elapsed_time_std', []).append(value)
				# FIXATIONS
				# fixations quantity
				view = df_trial_fixations_summary.iloc[idx_exp]['fix_total']
				value = sum(view) # total fixations
				d_rows.setdefault(exp+'_fix_total', []).append(value)
				value = view.mean() # mean fixations
				d_rows.setdefault(exp+'_fix_mean', []).append(value)
				value = view.std() # std fixations
				d_rows.setdefault(exp+'_fix_std', []).append(value)
				# fixations duration (by fixation)
				view = df_trial_fixations_summary.iloc[idx_exp]['fix_duration_total'] / df_trial_fixations_summary.iloc[idx_exp]['fix_total']
				value = view.mean() # mean duration
				d_rows.setdefault(exp+'_fix_duration_mean', []).append(value)
				value = view.std() # std duration
				d_rows.setdefault(exp+'_fix_duration_std', []).append(value)
				# fixations duration grouped by trial
				view = df_trial_fixations_summary.iloc[idx_exp]['fix_duration_total']
				value = sum(view) # total duration
				d_rows.setdefault(exp+'_fix_duration_trial_sum', []).append(value)
				value = view.mean() # mean duration
				d_rows.setdefault(exp+'_fix_duration_trial_mean', []).append(value)
				value = view.std() # std duration
				d_rows.setdefault(exp+'_fix_duration_trial_std', []).append(value)
				# gaze points (by fixation)
				view = df_trial_fixations_summary.iloc[idx_exp]['fix_gazep_total'] / df_trial_fixations_summary.iloc[idx_exp]['fix_total']
				value = view.mean() # mean gaze points
				d_rows.setdefault(exp+'_fix_gazep_mean', []).append(value)
				value = view.std() # std gaze points
				d_rows.setdefault(exp+'_fix_gazep_std', []).append(value)
				# gaze points grouped by trial
				view = df_trial_fixations_summary.iloc[idx_exp]['fix_gazep_total']
				value = sum(view) # total gaze points
				d_rows.setdefault(exp+'_fix_gazep_trial_sum', []).append(value)
				value = view.mean() # mean gaze points
				d_rows.setdefault(exp+'_fix_gazep_trial_mean', []).append(value)
				value = view.std() # std gaze points
				d_rows.setdefault(exp+'_fix_gazep_trial_std', []).append(value)

				# By Gender (given face expression)
				for g in gender:
					# answers
					view = participant_data[(participant_data['gender']==g) & (participant_data['expression']==exp)]
					idx_gen_exp = view.index.to_list()
					value = sum(view['ans_match'])
					d_rows.setdefault(exp+'_'+g+'_correct', []).append(value)
					value = view['ans_match'].mean() 
					d_rows.setdefault(exp+'_'+g+'_acc', []).append(value)
					value = view['answer_q2_numeric'].mean() 
					d_rows.setdefault(exp+'_'+g+'_conf', []).append(value)
					# elapsed time
					view = participant_data[(participant_data['gender']==g) & (participant_data['expression']==exp)]['elapsed_time']
					value = sum(view)
					d_rows.setdefault(exp+'_'+g+'_elapsed_time_total', []).append(value)
					value = view.mean()
					d_rows.setdefault(exp+'_'+g+'_elapsed_time_mean', []).append(value)
					value = view.std()
					d_rows.setdefault(exp+'_'+g+'_elapsed_time_std', []).append(value)
					# FIXATIONS
					# fixations quantity
					view = df_trial_fixations_summary.iloc[idx_gen_exp]['fix_total']
					value = sum(view) # total fixations
					d_rows.setdefault(exp+'_'+g+'_fix_total', []).append(value)
					value = view.mean() # mean fixations
					d_rows.setdefault(exp+'_'+g+'_fix_mean', []).append(value)
					value = view.std() # std fixations
					d_rows.setdefault(exp+'_'+g+'_fix_std', []).append(value)
					# fixations duration (by fixation)
					view = df_trial_fixations_summary.iloc[idx_gen_exp]['fix_duration_total'] / df_trial_fixations_summary.iloc[idx_gen_exp]['fix_total']
					value = view.mean() # mean duration
					d_rows.setdefault(exp+'_'+g+'_fix_duration_mean', []).append(value)
					value = view.std() # std duration
					d_rows.setdefault(exp+'_'+g+'_fix_duration_std', []).append(value)
					# fixations duration grouped by trial
					view = df_trial_fixations_summary.iloc[idx_gen_exp]['fix_duration_total']
					value = sum(view) # total duration
					d_rows.setdefault(exp+'_'+g+'_fix_duration_trial_sum', []).append(value)
					value = view.mean() # mean duration
					d_rows.setdefault(exp+'_'+g+'_fix_duration_trial_mean', []).append(value)
					value = view.std() # std duration
					d_rows.setdefault(exp+'_'+g+'_fix_duration_trial_std', []).append(value)
					# gaze points (by fixation)
					view = df_trial_fixations_summary.iloc[idx_gen_exp]['fix_gazep_total'] / df_trial_fixations_summary.iloc[idx_gen_exp]['fix_duration_total']
					value = view.mean() # mean gaze points
					d_rows.setdefault(exp+'_'+g+'_fix_gazep_mean', []).append(value)
					value = view.std() # std gaze points
					d_rows.setdefault(exp+'_'+g+'_fix_gazep_std', []).append(value)
					# gaze points grouped by trial
					view = df_trial_fixations_summary.iloc[idx_gen_exp]['fix_gazep_total']
					value = sum(view) # total gaze points
					d_rows.setdefault(exp+'_'+g+'_fix_gazep_trial_sum', []).append(value)
					value = view.mean() # mean gaze points
					d_rows.setdefault(exp+'_'+g+'_fix_gazep_trial_mean', []).append(value)
					value = view.std() # std gaze points
					d_rows.setdefault(exp+'_'+g+'_fix_gazep_trial_std', []).append(value)

			d_rows.setdefault('calibration', []).append(participant.calibration)
		results_df = pd.DataFrame.from_dict(d_rows)
		if export:
			results_df.to_excel(r'Export\view_participant.xlsx')
		self.df_participant_view = results_df

	def export_participant_view(self):
		if self.df_participant_view is not None:
			self.df_participant_view.to_excel(r'Export\view_participant.xlsx')

	def import_participant_view(self):
		try:
			self.df_participant_view = pd.read_excel(r"DataSource\view_participant.xlsx")
		except:
			print('Unexpected error: Import file view_participant.xlsx not found in DataSource directory.')
			exit(1)

	def remove_participants(self, remove_list):
		self.df_participant_view = self.df_participant_view[~self.df_participant_view['num_id'].isin(remove_list)] # remove outliers
		self.df_participant_view.reset_index(drop=True, inplace=True) # reset index
		self.df_trial_view = self.df_trial_view[~self.df_trial_view['num_id'].isin(remove_list)] # remove outliers
		self.df_trial_view.reset_index(drop=True, inplace=True) # reset index
		
		#views.experiment = views.experiment[~views.experiment['num_id'].isin(remove_list)] # remove outliers
		for i in reversed(range(len(self.experiment))):
			if self.experiment[i].num_id in remove_list:
				del self.experiment[i]
