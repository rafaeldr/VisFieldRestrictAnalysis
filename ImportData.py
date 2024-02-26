import os
import glob
import json
import pandas as pd
import pickle
import ParticipantResults as pr
from datetime import datetime

def import_loop(path, num_trials):

	exp_path = os.path.join(path, "*.csv")
	et_path = os.path.join(path, "*.txt")

	exp_files = glob.glob(exp_path)
	et_files = glob.glob(et_path)
	
	exp_files.sort(key=os.path.getmtime)
	et_files.sort(key=os.path.getmtime)

	experiment = []
	num_id = 1

	invalid_participants = []
	invalid_participants_files = []

	# Check files consistency
	if len(exp_files) != len(et_files):
		print('Unexpected error: Number of EyeTracking files does not match number of Experiment files.')
		exit(1)

	# Read experimental files (exp + et)
	for f in range(len(exp_files)):
		print('Reading file: '+exp_files[f])
		df_exp = pd.read_csv(exp_files[f], sep=';', encoding='utf-8')
		print('Reading file: '+et_files[f])
		
		# Import RAW eye tracking data (JSON) : one JSON object per line
		json_list = []
		with open(et_files[f], encoding='utf-8') as json_file:
			for json_line in json_file:
				json_list.append(json.loads(json_line))
		print('JSON object count: '+str(len(json_list)))

		# Create participant object
		participant = pr.ParticipantResults(df_exp['participant'][0], df_exp['StartExperiment'][0], df_exp['EndExperiment'].iloc[-1], 
									        df_exp['calibration'][0], switch_exp_terminology(df_exp['expName'][0]), num_trials)

		# Create trials data frame
		try:
			df_trials = df_exp[['imageFile_Faces','Expressions','trials.thisIndex','StartRoutine','EndRoutine',
								'StartQ1','EndQ1','Resp_Q1.keys','StartQ2','EndQ2','Resp_Q2.keys']][1:num_trials+1]
		except:
			df_trials = df_exp[['imageFile_Tudo','Expressions','trials.thisIndex','StartRoutine','EndRoutine',
								'StartQ1','EndQ1','Resp_Q1.keys','StartQ2','EndQ2','Resp_Q2.keys']][1:num_trials+1]

		df_trials.rename(columns={'imageFile_Faces': 'image_file'}, inplace = True)
		df_trials.rename(columns={'imageFile_Tudo': 'image_file'}, inplace = True)
		df_trials.rename(columns={'Expressions': 'expression'}, inplace = True)
		df_trials.rename(columns={'trials.thisIndex': 'trial_id'}, inplace = True)
		df_trials['trial_id'] = df_trials['trial_id'].astype(int)
		df_trials.rename(columns={'StartRoutine': 'start_time'}, inplace = True)
		df_trials.rename(columns={'EndRoutine': 'end_time'}, inplace = True)
		df_trials.rename(columns={'StartQ1': 'start_q1'}, inplace = True)
		df_trials.rename(columns={'EndQ1': 'end_q1'}, inplace = True)
		df_trials.rename(columns={'Resp_Q1.keys': 'answer_q1'}, inplace = True)
		df_trials.rename(columns={'StartQ2': 'start_q2'}, inplace = True)
		df_trials.rename(columns={'EndQ2': 'end_q2'}, inplace = True)
		df_trials.rename(columns={'Resp_Q2.keys': 'answer_q2'}, inplace = True)
		df_trials.reset_index(drop=True, inplace = True)

		# Processing Eye Tracking data
		print('Processing Eye Tracking data...')
		for i in range(num_trials):
			# Adjusting data values
			file_path = df_trials['image_file'].iloc[i]
			head, tail = os.path.split(file_path)
			df_trials.loc[i, 'image_file'] = tail

			expression_temp = df_trials['expression'].iloc[i]
			df_trials.loc[i, 'expression'] = switch_expression_terminology(expression_temp)

			ans_q1 = df_trials['answer_q1'].iloc[i]
			df_trials.loc[i, 'answer_q1'] = switch_answer_emotion(ans_q1)

			ans_q2 = df_trials['answer_q2'].iloc[i]
			df_trials.loc[i, 'answer_q2'] = switch_answer_certainty(ans_q2)

			# Eye tracking data cutting
			dt_format = "%Y-%m-%d %H:%M:%S.%f"
			start_time = datetime.strptime(df_trials['start_time'].iloc[i], dt_format)
			end_time = datetime.strptime(df_trials['end_time'].iloc[i], dt_format)
			et_data_local = []
			to_be_removed = []
			for j in range(len(json_list)):
				print('Trial: '+str(i+1)+'/'+str(num_trials)+'. Processing Eye Tracker file line '+str(j+1)+' of '+str(len(json_list))+' \r', end="")
				# Check if is an eye tracking record
				if json_list[j]['category'] == 'tracker' and json_list[j]['statuscode'] == 200:
					et_time =  datetime.strptime(json_list[j]['values']['frame']['timestamp'], dt_format)
					
					if et_time >= start_time and et_time <= end_time:
						et_data = parse_JSON(json_list[j], et_data_local)
						to_be_removed.append(j)
			# Format list as DataFrame
			df_et = pd.DataFrame(et_data_local)
			#df_et.to_excel('et_trial_debug.xlsx') # DEBUG (excel messes up the datetime), use csv instead
			df_et['timestamp'] = pd.to_datetime(df_et['timestamp'], format=dt_format)
			
			# Remove processed lines from JSON list (fastest way)
			for j in sorted(to_be_removed, reverse=True):
				del json_list[j]

			# Append trial data to participant
			participant.append_et_data(df_et)
		
		# Set experiment data to participant
		participant.set_experiment_data(df_trials)
		
		print()
		print()

		if not participant.is_invalid:
			participant.num_id = num_id
			experiment.append(participant)
			num_id += 1
		else:
			print('Participant is invalid. Skipping...')
			# invalid at this point has no num_id
			invalid_participants.append(participant)
			invalid_participants_files.append(exp_files[f])
			invalid_participants_files.append(et_files[f])

	print('All files processed with no errors!')
	print('Invalid participants (discarded): '+str(len(invalid_participants)))

	# Expunge invalid participants
	with open('Export/invalid_participants.pkl', 'wb') as output:
		pickle.dump(invalid_participants, output, pickle.HIGHEST_PROTOCOL)
	df_export = pd.DataFrame(invalid_participants_files)
	df_export.to_excel('Export/invalid_participants_files.xlsx')

	return experiment
		
def switch_answer_emotion(ans):
	if ans == 'num_1':
		return 'Happiness'
	elif ans == 'num_2':
		return 'Sadness'
	elif ans == 'num_3':
		return 'Neutrality'
	elif ans == 'num_4':
		return 'Fear'
	elif ans == 'num_5':
		return 'Anger'
	else:
		print('Error: Invalid answer')
		exit(1)

def switch_answer_certainty(ans):
	if ans == 'num_1':
		return 'Strongly agree' # 'Yes, sure' | 'Sim, com certeza'
	elif ans == 'num_2':
		return 'Agree' # 'Yes, with doubt' | 'Sim, com dúvida'
	elif ans == 'num_3':
		return 'Not sure' # 'I can’t say' | 'Não sei dizer'
	elif ans == 'num_4':
		return 'Disagree' # 'No, with doubt' | 'Não, com dúvida'
	elif ans == 'num_5':
		return 'Strongly disagree' # 'No, sure' | 'Não, com certeza'
	else:
		print('Error: Invalid answer')
		exit(1)

def switch_exp_terminology(ans):
	if ans == 'SR' or ans == 'NVR':
		return 'NVR'
	elif ans == 'RM' or ans == 'PFFV':
		return 'PFFV'
	elif ans == 'RP' or ans == 'FV':
		return 'FV'
	else:
		print('Error: Invalid experiment terminology')
		exit(1)

def switch_expression_terminology(ans):
	if ans == 'Felicidade' or ans == 'Happiness':
		return 'Happiness'
	elif ans == 'Tristeza' or ans == 'Sadness':
		return 'Sadness'
	elif ans == 'Neutra'  or ans == 'Neutrality':
		return 'Neutrality'
	elif ans == 'Medo' or ans == 'Fear':
		return 'Fear'
	elif ans == 'Raiva' or ans == 'Anger':
		return 'Anger'
	else:
		print('Error: Invalid expression terminology')
		exit(1)

def parse_JSON(json_record, et_list) -> int:
	
	# Parse row and append to data frame
	base = json_record['values']['frame']

	row = pd.Series({'avg_x': base['avg']['x'],
					 'avg_y': base['avg']['y'],
					 'raw_x': base['raw']['x'],
					 'raw_y': base['raw']['y'],
					 'fix': base['fix'],
					 'lefteye_avg_x': base['lefteye']['avg']['x'],
					 'lefteye_avg_y': base['lefteye']['avg']['y'],
					 'lefteye_pupil_center_x': base['lefteye']['pcenter']['x'],
					 'lefteye_pupil_center_y': base['lefteye']['pcenter']['y'],
					 'lefteye_pupil_size': base['lefteye']['psize'],
					 'lefteye_raw_x': base['lefteye']['raw']['x'],
					 'lefteye_raw_y': base['lefteye']['raw']['y'],
					 'righteye_avg_x': base['righteye']['avg']['x'],
					 'righteye_avg_y': base['righteye']['avg']['y'],
					 'righteye_pupil_center_x': base['righteye']['pcenter']['x'],
					 'righteye_pupil_center_y': base['righteye']['pcenter']['y'],
					 'righteye_pupil_size': base['righteye']['psize'],
					 'righteye_raw_x': base['righteye']['raw']['x'],
					 'righteye_raw_y': base['righteye']['raw']['y'],
					 'state' : base['state'],
					 'time' : base['time'],
					 'timestamp': base['timestamp']})

	et_list.append(row)

	return et_list