import pandas as pd
from datetime import datetime
import peyemmv
import ImageStimulus as ims

class ParticipantResults:

	def __init__(self, participant_id, time_start, time_end, calibration, exp_type, num_trials):

		self.participant_id = participant_id	# Name of the participant
		self.num_id = -1						# Id of the participant (later assigned)
		self.time_start = time_start			# Time of the start of the experiment
		self.time_end = time_end				# Time of the end of the experiment
		self.calibration = calibration			# Calibration score (1-5)
		self.num_trials = num_trials			# Number of trials
		if exp_type in ['FV', 'PFFV', 'NVR']:
			self.exp_type = exp_type			# Type of experiment (RP, RM, SR)
		else:
			print('Unexpected error: Invalid experiment type.')
			exit(1)
		
		self.experiment_data = []				# DataFrame for trials
		self.et_data = []						# Eye-tracking data (x30)
		self.et_data_dirty = []					# Eye-tracking data (x30) [As acquired from the eye-tracker] -> Created only after data cleaning
		self.fixations_data = []				# Fixations (x30)

		# Parameter for Fixations Calculation [Same from Matlab]
		#xmax= 1920
		#ymax= 1080
		self.t1 = 40
		self.t2 = 40
		self.tdur = 80

		# Parameter for Fixation Data Cleaning
		self.is_clean = True # Flag to indicate if the data is clean or not (or activate/deactivate the cleaning)
		self.xmax= 1920
		self.ymax= 1080

		self.is_invalid = False					# Flag to indicate if the data is invalid (e.g. missing trials)
	
	def set_experiment_data(self, df):
		self.experiment_data = df
		self.post_import_experiment_data_adjustment()

	def append_et_data(self, et_trial):
		if self.is_clean:
			self.et_data_dirty.append(et_trial.copy(deep=True))

			# Find zero values
			idx_zeros = et_trial[((et_trial['avg_x']==0)&(et_trial['avg_y']==0))].index
			et_trial.drop(idx_zeros, axis=0, inplace=True)

			# Find values outside the screen
			idx_outside = et_trial[((et_trial['avg_x']<0)|(et_trial['avg_x']>self.xmax)|(et_trial['avg_y']<0)|(et_trial['avg_y']>self.ymax))].index
			et_trial.drop(idx_outside, axis=0, inplace=True)
			
			# Adjust indexing
			et_trial.reset_index(inplace=True, drop=True) 
		
		if len(et_trial) == 0:
			self.is_invalid = True
		self.et_data.append(et_trial)

	def et_data_cleaning(self):
		pass

	def format_for_fixation(et_data) -> list:
		df_et_trial = et_data[['avg_x','avg_y','time']]
		df_et_trial.reset_index(drop=True, inplace = True)
		#df_et_trial.to_csv('et_trial.csv', sep=' ', encoding='utf-8', index=False) # DEBUG
		list_trial = df_et_trial.values.tolist()
		return list_trial

	def set_fixation_parameters(self, t1 = 40, t2 = 40, tdur = 80):
		self.t1 = t1
		self.t2 = t2
		self.tdur = tdur

	def calcutate_fixation_data(self):
		#for t in self.et_data:
		for t in range(len(self.et_data)):
			print('Calculating Fixations for Trial: '+str(t+1)+'/'+str(len(self.et_data))+' \r', end="")
			# Expected format: (x,y,passing time)
			t_f = ParticipantResults.format_for_fixation(self.et_data[t])
			fixations = peyemmv.extract_fixations(t_f, t1 = self.t1, t2 = self.t2, min_dur = self.tdur, report_fix = False)
			#fixations = peyemmv.extract_fixations(t, t1 = self.t1, t2 = self.t2, min_dur = self.tdur, report_fix = True) # DEBUG
			#fix_csv = pd.DataFrame(fixations) # DEBUG
			#fix_csv.to_csv('fix.csv', sep=' ', encoding='utf-8', index=False) # DEBUG
			self.fixations_data.append(fixations)
		print()

	def post_import_experiment_data_adjustment(self):
		# Answer Certainty (Numeric Value)
		answer_q2_numeric = self.experiment_data['answer_q2']
		answer_q2_numeric = [switch_reverse_answer_certainty_numeric(x) for x in answer_q2_numeric]
		self.experiment_data['answer_q2_numeric'] = answer_q2_numeric
		# Face Gender
		image_files = self.experiment_data['image_file']
		gender = [x[1] for x in image_files]
		self.experiment_data['gender'] = gender
		# Answer Correct?
		ans_match = self.experiment_data['expression']==self.experiment_data['answer_q1']
		self.experiment_data['ans_match'] = ans_match
		# Time
		dt_format = "%Y-%m-%d %H:%M:%S.%f"
		end_time = self.experiment_data['end_time']
		end_time = pd.Series([datetime.strptime(x, dt_format) for x in end_time])
		start_time = self.experiment_data['start_time']
		start_time = pd.Series([datetime.strptime(x, dt_format) for x in start_time])
		elapsed_time = end_time-start_time
		elapsed_time = [x.total_seconds() for x in elapsed_time]
		self.experiment_data['elapsed_time'] = elapsed_time
		#self.experiment_data.to_excel('debug.xlsx')


	def show_image_from_trial(self, trial_id, mode = 'f'):
		if trial_id < 0 or trial_id >= len(self.experiment_data):
			print('Unexpected error: Trial id exceeds its limits.')
			exit(1)
		# Image
		image_file = self.experiment_data['image_file'][trial_id]

		# Fixations
		if mode == 'f' or mode == 'h':
			fixations = self.fixations_data[trial_id]
		else:
			fixations = []
		if mode == 'e' or mode == 'h':
			et_raw = ParticipantResults.format_for_fixation(self.et_data[trial_id])
		else:
			et_raw = []

		ims.show_image(image_file, fixations, et_raw)

def switch_reverse_answer_certainty_numeric(ans):
	if ans == 'Strongly agree':
		return 1
	elif ans == 'Agree':
		return 2
	elif ans == 'Not sure':
		return 3
	elif ans == 'Disagree':
		return 4
	elif ans == 'Strongly disagree':
		return 5
	else:
		print('Error: Invalid answer')
		exit(1)
