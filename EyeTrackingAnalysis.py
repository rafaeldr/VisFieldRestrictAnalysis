import os
import ImportData
import pickle
import time
import ExperimentViews as ev
import AnalysisContainer as ac

def main():

	# Parameters
	num_trials = 30
	raw_enabled = False

	# Create folder structure
	isExist = os.path.exists(r"DataSource")
	if not isExist: os.makedirs(r"DataSource")

	isExist = os.path.exists(r"Export")
	if not isExist: os.makedirs(r"Export")

	isExist = os.path.exists(r"Export\Figures")
	if not isExist: os.makedirs(r"Export\Figures")

	import_path = r"DataSource"

	exp_types = ['FV', 'PFFV', 'NVR']

	expressions = ['Happiness', 'Sadness', 'Neutrality', 'Fear', 'Anger']
	
	# Two participants were (manually) removed from the experiment due to technical issues with data files

	# Import data
	if raw_enabled:
		if os.path.exists('Export/experiment.pkl'):
			print('Loading pre-processed experiment object...')
			with open('Export/experiment.pkl', 'rb') as file_input:
				experiment = pickle.load(file_input)
		else:
			start_time = time.time()
			experiment = ImportData.import_loop(import_path, num_trials)
		
			# Calculate Fixations
			for p in range(len(experiment)):
				print('Participant: '+str(p+1))
				experiment[p].calcutate_fixation_data()
		
			print("--- %s seconds ---" % (time.time() - start_time))
			# Save experiment object
			with open('Export/experiment.pkl', 'wb') as output:
				pickle.dump(experiment, output, pickle.HIGHEST_PROTOCOL)

		# One participant was removed after data cleaning

		# Export Global Data (and start ExperimentViews object)
		views = ev.ExperimentViews(experiment, exp_types, expressions)
		views.generate_participant_view(export = False)
		views.generate_trial_view(export = False)

		# Data analysis - outliers
		ac.outlier_analysis(views)

		# RE-Export Global Data (without outliers)
		views.export_participant_view()
		views.export_trial_view()
	else:
		print('Loading pre-processed view spreadsheets...')
		views = ev.ExperimentViews(None, exp_types, expressions)
		views.import_participant_view()
		views.import_trial_view()

	# Confusion Matrix for expression judgement
	ac.confusion_analysis(views)

	# Confusion Matrix for expression judgement by facial gender
	ac.confusion_analysis_by_gender(views)

	# Violin Plot by Experiment Condition
	ac.violin_plot_by_exp_condition(views)

	# Violin Plot by Facial Gender
	ac.violin_plot_by_gender(views)

	ac.dealocate_analysis_objects()
	input('Press any key to finish...')

if __name__ == '__main__':
	main()