from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QHBoxLayout, QPushButton, QComboBox, QCheckBox, QTextEdit, QStatusBar, 
    QScrollArea, QFrame, QButtonGroup)
from PySide6.QtCore import Qt
import sys
import os
import pandas as pd
import users
import questions
import questionscore
import wordassociation
import graphics
import powerpoint

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Griefleader Analysis")
        self.setFixedSize(1000, 720)
        self.base_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                     'desktop-application', 'app', 'files')
        self.selected_files = {}
        self.setup_ui()
        self.load_folders()

    def setup_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        
        # Left Panel
        left_panel = QVBoxLayout()
        left_panel.setContentsMargins(10, 10, 10, 10)
        left_panel.setSpacing(5)  # Reduced spacing between dropdown and files area
        
        self.file_dropdown = QComboBox()
        self.file_dropdown.setFixedWidth(200)
        self.file_dropdown.currentTextChanged.connect(self.populate_files)
        left_panel.addWidget(self.file_dropdown)
        
        self.files_area = QScrollArea()
        self.files_widget = QWidget()
        self.files_layout = QVBoxLayout(self.files_widget)
        self.files_layout.setSpacing(2)  # Minimal spacing between checkboxes
        self.files_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        self.files_layout.setAlignment(Qt.AlignTop)
        self.files_area.setWidget(self.files_widget)
        self.files_area.setWidgetResizable(True)
        self.files_area.setFrameStyle(QFrame.StyledPanel)
        self.files_area.setFixedWidth(200)
        left_panel.addWidget(self.files_area)
        
        left_container = QWidget()
        left_container.setLayout(left_panel)
        main_layout.addWidget(left_container)
        
        # Right Panel
        right_panel = QVBoxLayout()
        right_panel.setSpacing(5)  # Reduced spacing
        buttons_layout = QHBoxLayout()
        
        self.load_btn = QPushButton("Load")
        self.load_btn.setFixedWidth(100)
        self.load_btn.setEnabled(False)
        buttons_layout.addWidget(self.load_btn)
        
        self.powerpoint_btn = QPushButton("Generate PowerPoint")
        self.powerpoint_btn.setFixedWidth(150)
        self.powerpoint_btn.setEnabled(False)
        buttons_layout.addWidget(self.powerpoint_btn)
        
        self.report_btn = QPushButton("Generate Report")
        self.report_btn.setFixedWidth(150)
        self.report_btn.setEnabled(False)
        buttons_layout.addWidget(self.report_btn)
        
        buttons_layout.addStretch()
        right_panel.addLayout(buttons_layout)
        
        self.preview = QTextEdit()
        self.preview.setReadOnly(True)
        self.preview.setMinimumSize(800, 500)
        right_panel.addWidget(self.preview, 1)  # Added stretch factor
        
        right_container = QWidget()
        right_container.setLayout(right_panel)
        main_layout.addWidget(right_container)
        
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        self.load_btn.clicked.connect(self.load_file)
        self.powerpoint_btn.clicked.connect(self.generate_powerpoint)
        self.report_btn.clicked.connect(self.generate_report)
        
        self.checkbox_group = QButtonGroup()
        self.checkbox_group.setExclusive(True)
        self.checkbox_group.buttonClicked.connect(self.handle_checkbox_change)
        
        self.status_bar.showMessage("Ready")

    def load_folders(self):
        try:
            self.file_dropdown.addItem("---Files---")
            folders = sorted([d for d in os.listdir(self.base_path) 
                            if os.path.isdir(os.path.join(self.base_path, d))])
            self.file_dropdown.addItems(folders)
        except FileNotFoundError:
            self.status_bar.showMessage("Error: Files directory not found")

    def populate_files(self, folder_type):
        if folder_type == "---Files---":
            return
        
        for i in reversed(range(self.files_layout.count())): 
            self.files_layout.itemAt(i).widget().setParent(None)
        
        folder_path = os.path.join(self.base_path, folder_type)
        try:
            files = sorted(os.listdir(folder_path))
            for file in files:
                checkbox = QCheckBox(file)
                self.files_layout.addWidget(checkbox)
                self.checkbox_group.addButton(checkbox)
                
                if folder_type in self.selected_files and file == self.selected_files[folder_type]:
                    checkbox.setChecked(True)
            
            if len(files) == 1 and folder_type not in self.selected_files:
                self.files_layout.itemAt(0).widget().setChecked(True)
                self.selected_files[folder_type] = files[0]
                
            self.check_load_button_state()
                
        except FileNotFoundError:
            self.status_bar.showMessage(f"Error: Folder {folder_type} not found")

    def handle_checkbox_change(self, checkbox):
        if checkbox.isChecked():
            current_folder = self.file_dropdown.currentText()
            self.selected_files[current_folder] = checkbox.text()
            self.check_load_button_state()

    def check_load_button_state(self):
        folders = [folder for folder in os.listdir(self.base_path) 
                  if os.path.isdir(os.path.join(self.base_path, folder))]
        self.load_btn.setEnabled(all(folder in self.selected_files for folder in folders))

    def display_df_info(self, df, name):
        self.preview.append(f"\n{name} DataFrame Info:")
        self.preview.append(f"Shape: {df.shape}")
        self.preview.append(f"Columns: {', '.join(df.columns)}")
        self.preview.append("First few rows:")
        self.preview.append(df.head().to_string())
        self.preview.append("\n" + "="*50 + "\n")

    def load_file(self):
        try:
            self.preview.clear()
            self.preview.append("Loading files...\n")
            
            userImportFiles = pd.read_csv(os.path.join(self.base_path, 'userimports', self.selected_files['userimports']))
            self.display_df_info(userImportFiles, "User Import")
            
            exportedDataFile = pd.read_csv(os.path.join(self.base_path, 'results', self.selected_files['results']))
            self.display_df_info(exportedDataFile, "Exported Data")
            
            self.qfile = pd.read_csv(os.path.join(self.base_path, 'questions', self.selected_files['questions']))
            self.display_df_info(self.qfile, "Questions")
            
            wordImportFile = pd.read_csv(os.path.join(self.base_path, 'words', self.selected_files['words']))
            self.display_df_info(wordImportFile, "Words")
            
            clusterImportFile = pd.read_csv(os.path.join(self.base_path, 'clusters', self.selected_files['clusters']))
            self.display_df_info(clusterImportFile, "Clusters")
            
            self.companyName = "Liberty University"
            
            self.preview.append("Processing data...\n")
            
            self.preview.append("Initializing user data...")
            self.userInfo = users.run(userImportFiles, exportedDataFile)
            del userImportFiles
            del exportedDataFile
            self.preview.append("User data initialized successfully\n")
            
            self.preview.append("Processing questions...")
            self.questionInfo = questions.run(self.qfile)
            self.preview.append("Questions processed successfully\n")
            
            self.preview.append("Calculating question scores...")
            self.questionAssessmentInfo = questionscore.run(self.userInfo[0], self.userInfo[1], 
                                                          self.userInfo[2], self.questionInfo)
            self.preview.append("Question scoring complete\n")
            
            self.preview.append("Processing word associations...")
            self.wordAssessmentInfo = wordassociation.run(wordImportFile, clusterImportFile, 
                                                         self.userInfo[0], self.userInfo[1], self.userInfo[2])
            del wordImportFile
            del clusterImportFile
            self.preview.append("Word associations processed successfully\n")
            
            self.powerpoint_btn.setEnabled(True)
            self.report_btn.setEnabled(True)
            
            self.preview.append("\nAll data processed successfully!")
            self.status_bar.showMessage("Data processing complete")
            
        except Exception as e:
            self.preview.append(f"\nError processing data: {str(e)}")
            self.status_bar.showMessage("Error in data processing")

    def generate_powerpoint(self):
        try:
            self.preview.append("\nGenerating graphics...")
            questionTable = graphics.run(self.questionAssessmentInfo, self.wordAssessmentInfo, 
                                      self.userInfo[1], self.userInfo[2], self.questionInfo, 
                                      self.companyName)
            
            self.preview.append("Creating PowerPoint presentation...")
            powerpoint.run(questionTable, self.companyName, self.qfile)
            
            self.preview.append("PowerPoint generation complete!")
            self.status_bar.showMessage("PowerPoint generated successfully")
        except Exception as e:
            self.preview.append(f"\nError generating PowerPoint: {str(e)}")
            self.status_bar.showMessage("PowerPoint generation failed")

    def generate_report(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())