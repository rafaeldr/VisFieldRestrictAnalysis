# Visual Field Restriction Data Analysis Software

## Software Description

This software was specifically designed to transform and analyze data collected for the experiment described in the section below.<br>
Note: It was not designed as a general-purpose eye tracking data analysis tool.

Key Features:
- Import and combine data from experiments conducted using the [Visual Field Restriction Data Collection Software](https://github.com/melinaurtado/VisFieldFacialExpCollect) with Eye Tribe’s ET1000 tracking data.
  - https://doi.org/10.5281/zenodo.10700824
- Perform data transformation and preprocessing tasks to prepare data for analysis.
- Implement various data analysis methods to explore the relationship between visual field restriction and facial expression recognition.
- Generate visualizations to aid in the interpretation of results.

## Experiment Description

**Title:** Visual Field Restriction in the Recognition of Basic Facial Expressions: A Combined Eye Tracking and Gaze Contingency Study

**Authors:** M. B. Urtado, R. D. Rodrigues, S. S. Fukusima

**Publication Link:** https://www.mdpi.com/2076-328X/14/5/355 <br>

- Urtado MB, Rodrigues RD, Fukusima SS. **Visual Field Restriction in the Recognition of Basic Facial Expressions: A Combined Eye Tracking and Gaze Contingency Study**. Behavioral Sciences. 2024;14: 355. doi:[10.3390/bs14050355](https://doi.org/10.3390/bs14050355)

In this experiment, participants were presented with 30 facial image stimuli under three visual field restriction conditions: NVR (No Visual Restriction), PFFV (Parafoveal and Foveal Vision), and FV (Foveal Vision).<br>
In the NVR condition, stimuli were presented without any restriction, while in the PFFV and FV conditions, the visual field was limited to 5° and 2° of the visual angle, respectively.<br>
The visual restriction was implemented using the moving window technique, directly controlled by the eye tracker in response to the viewer’s eye gaze (this is controlled by the eye tracker driver, not the experiment software).<br>
For all conditions, the eye movements were constantly recorded (again directly by the eye tracker driver).<br>
The goal was to investigate the impact of visual field restriction on the recognition of basic facial expressions.<br>
<br>
Note: This README.md section provides a brief overview of the experiment, for more detailed information, please refer to the publication once it is available.

## Requirements

1. Install Anaconda package manager.
   - https://www.anaconda.com/download
2. Create a new Python environment importing the "requirements.yaml" file.
   - We suggest the environment name: py3_eye
3. The main execution file is: "EyeTrackingAnalysis.py"
4. If you want to replicate the results presented in the above manuscript:
   - Copy the following data files from: https://doi.org/10.5281/zenodo.10703513
     - view_trial.xlsx
     - view_participant.xlsx
   - Put these data files in the folder /DataSource/ inside the project directory.
5. OPTIONAL: Download the required facial images directly from [The Karolinska Directed Emotional Faces (KDEF)](https://kdef.se/).
   - Replace the 30 dummy images located in the "./Images/" directory of this repository with the newly downloaded images according to the respective IDs indicated by file names (also see "Image IDs" on "Project Organization").
   - These 30 images need to be converted to grayscale to replicate our exact experiment.
   - Note: This is optional since the main route of data analysis does not call these images.

## Software Environment

- **Language:** Python 3.10
- **Environment Manager:** Anaconda
- **Environment Name:** py3_eye
- **Version Control:** GitHub
- **IDE:** Visual Studio Community 2022
- **Used Libraries:**
  - Data Manipulation: NumPy, Pandas
  - Visualization: Matplotlib, Seaborn, OpenCV
  - Batch Processing: Glob*, Pickle*
  <br>\* Built-in Python Modules
  - Export: Openpyxl
  - Others: Scipy, Sklearn
- **Third-Party Code:** PeyeMMV
- **Operating System:** Microsoft Windows 10

## Third Party Software

**Peyemmv:** *"PeyeMMV constitutes a Python module that implements the two-step spatial dispersion fixation detection algorithm imported in both EyeMMV and LandRate MATLAB toolboxes. Specifically, this algorithm implements spatiotemporal criteria, belongs to the family of I-DT based algorithms and can be used as a spatial noise filtering approach during fixation identification process. PeyeMMV module could be utilized in order to extract fixation clusters among raw gaze data as well as to generate a basic plot that visualizes both gaze data and fixation centers positions. The module could be easily imported in every Python script or module."*

- https://github.com/SoftwareImpacts/SIMPAC-2022-305
- KRASSANAKIS, V. PeyeMMV: Python implementation of EyeMMV’s fixation detection algorithm. Software Impacts, v. 15, p. 100475, 2023. DOI: https://doi.org/10.1016/j.simpa.2023.100475. 

## Project Organization

- **The directory structure of the project is:**
  - **VisFieldRestrictAnalysis/:**  the root directory. All Python files are here.
  - **./DataSource/:** where the input data must be. Here you must copy the data you will process.
  - **./Export/:** where all output will be saved.
  - **./Export/Figures:** where the generated figures are saved.
  - **./Images/:** where the facial images analyzed by the participants must be copied.
    - **Note on Image Usage:** The original experiment utilized images from The Karolinska Directed Emotional Faces (KDEF) image database. However, **due to licensing restrictions, these images cannot be included in this repository**. As an alternative, we replaced the KDEF images with dummy synthetic facial images obtained from [ThisPersonDoesNotExist.com](https://thispersondoesnotexist.com/) converted to grayscale (**these were not used in the research experiment**). The file names were maintained to keep compatibility with the original experiment source code. These synthetic images have no research value and are not paired with the expected emotional expressions; they were included only to demonstrate the software functionality, allowing you to run it. Please, refer to "Requirements" to change these files to the correct ones from KDEF.
    - Goeleven, E.; Raedt, R.D.; Leyman, L.; Verschuere, B. The Karolinska Directed Emotional Faces: A validation study. Cognition and Emotion 2008, 22, 1094–1118. https://doi.org/10.1080/02699930701626582.
    - Lundqvist, D.; Flykt, A.; Öhman, A. The Karolinska Directed Emotional Faces - KDEF - CD ROM from Department of Clinical Neuroscience, 1998.
    - https://kdef.se/
    - Image IDs: AF01HAS, AM02HAS, AF02HAS, AM04HAS, AF06HAS, AM31HAS, AF03SAS, AM16SAS, AF07SAS, AM25SAS, AF17SAS, AM32SAS, AF04NES, AM05NES, AF08NES, AM07NES, AF16NES, AM13NES, AF13AFS, AM08AFS, AF14AFS, AM14AFS, AF21AFS, AM23AFS, AF05ANS, AM10ANS, AF09ANS, AM17ANS, AF20ANS, AM29ANS.

- **Project files are:**
  - **EyeTrackingAnalysis.py:** Main python file.
  - **ImportData.py:** Import data from the experiment and eye tracker files (if present).
  - **ParticipantResults.py:** Represents the data from each participant (object-oriented).
  - **ExperimentViews.py:** Create the main views for the data analyzed by the program. There are two: df_trial_view and df_participant_view.
  - **StatsContainer.py:** Currently contains only the outlier detection analysis.
  - **AnalysisContainer.py:** A container for all data analysis steps (in distinct static methods).
  - **peyemmv.py:** Third-party code required to extract fixations from raw eye tracking data (see "Third Party Software" section).
  - **ImageStimulus.py:** Adjust the stimulus (face image) for plotting. * Not used in this research project.
  - **requirements.yaml:** The environment description file from Anaconda. Contains all package versions used.

- **Expected behavior / How to use:**
  1. **Replicate data analysis:** Just follow the basic instructions in the requirements section, including the "view_trial.xlsx" and "view_participant.xlsx" files in the DataSource directory.
  2. **Replicate the complete experiment with your participant data:**
     1. Properly set the experiment software: https://github.com/melinaurtado/VisFieldFacialExpCollect following specific recommendations.
     2. Run the experiment and collect your data. Assure to configure your eye tracking device with the manufacturer driver to start recording after calibration.
        - Note: This code was designed to work with the exact Eye Tracker model and collector software in https://github.com/melinaurtado/VisFieldFacialExpCollect.
        - The experiment and trial data are synchronized based on the machine clock timestamps on both files.
     4. Each participant must have two files, one from the PsychoPy experiment (.csv) and one from the raw eye tracking (.txt).
     5. The files from all collected participants must be processed at once.
        - No extra file should be in the DataSource directory for this operation mode.
        - The files are captured according to the modified time, so you should not manually edit any file. (This is rigid to avoid mixing participants' files)
     6. To enable this mode, change line 12 from the EyeTrackingAnalysis.py to "raw_enabled = True".

## License

This software is released under the GNU General Public License Version 3.

## Research Ethics Committee

The study was approved by the Research Ethics Committee (CEP) of the University of São Paulo (protocol code 41844720.5.0000.5407). 
