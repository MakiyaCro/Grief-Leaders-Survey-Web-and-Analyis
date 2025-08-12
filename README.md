# Cultural Assessment Leadership Team Review

A comprehensive Python desktop application for analyzing employee cultural assessment surveys and generating detailed PowerPoint presentations and individual PDF reports.

## Overview

This application processes employee survey data to create visual analytics and insights about organizational culture across different categories:
- **RFP** (Respect for People)
- **EPS** (Emotional Wellbeing) 
- **CM** (Change Management)
- **LdrSpv** (Leadership Supervisor)
- **SrLdr** (Senior Leaders)

## Features

### Core Functionality
- **Data Processing**: Imports and processes user data, survey responses, questions, and word associations
- **Visual Analytics**: Generates charts, graphs, dial indicators, and participation analysis
- **PowerPoint Generation**: Creates comprehensive presentation slides with embedded visualizations
- **Individual Reports**: Generates personalized PDF reports for each participant
- **Word Association Analysis**: Analyzes sentiment and word clustering from survey responses

### Key Visualizations
- Participation graphs by department and position
- Dial charts showing performance scores across categories
- Question analysis tables with statistical highlighting
- Word association matrices and gradients
- Cluster analysis tables for positive/negative sentiment


## Directory Structure

```
desktop-application/
└── app/
    ├── files/
    │   ├── userimports/     # User data CSV files
    │   ├── results/         # Survey response CSV files
    │   ├── questions/       # Question definition CSV files
    │   ├── words/           # Word association CSV files
    │   └── clusters/        # Word cluster definition CSV files
    ├── graphics/
    │   ├── dials/           # Generated dial charts
    │   ├── participation/   # Participation graphs
    │   ├── questiongraphs/  # Question analysis charts
    │   ├── questiontables/  # Question data tables
    │   ├── wordchart/       # Word association charts
    │   ├── wordgraphs/      # Word analysis graphs
    │   ├── wordtables/      # Word data tables
    │   ├── clustertables/   # Cluster analysis tables
    │   └── gradient/        # Word gradient visualizations
    ├── powerpoint/
    │   ├── empty.pptx       # Template presentation
    │   └── test.pptx        # Generated output
    └── report/
        └── template.docx    # Individual report template
```

## Usage

### GUI Application
```bash
python maingui.py
```

1. **Load Files**: Select data files from dropdown menus
2. **Process Data**: Click "Load" to process all selected files
3. **Generate PowerPoint**: Create comprehensive presentation
4. **Generate Reports**: Create individual PDF reports (if implemented)

### Command Line
```bash
python app.py
```

## Data File Requirements

### User Import File (CSV)
Required columns:
- `username`, `email`, `first_name`, `last_name`
- `company`, `location`, `status`, `department`
- `hipo`, `manager`, `password`

### Survey Results File (CSV)
- Must contain `User Name` column
- Survey responses in subsequent columns
- Word associations in final column (comma-separated)

### Questions File (CSV)
Required columns:
- `qNum`: Question number
- `qScore`: Question weight/score
- `qCat`: Category (RFP, EPS, CM, LdrSpv, SrLdr)
- `qSubCat`: Subcategory
- `descript`: Question description

### Words File (CSV)
Required columns:
- `word`: Word text
- `ident`: Identifier (pos/neg for positive/negative)

### Clusters File (CSV)
Required columns:
- `groupname`: Cluster name
- `ident`: Cluster identifier (p/n)
- `words`: Comma-separated list of words in cluster

## Key Components

### Core Modules
- **`users.py`**: User data management and processing
- **`questions.py`**: Question data handling
- **`questionscore.py`**: Survey response scoring and analysis
- **`wordassociation.py`**: Word sentiment and cluster analysis
- **`graphics.py`**: Visualization generation
- **`powerpoint.py`**: PowerPoint presentation creation
- **`report.py`**: Individual PDF report generation

### GUI Interface
- **`maingui.py`**: PySide6-based desktop application interface

## Configuration

### Company Settings
Update the `companyName` variable in relevant files to customize for your organization.

### Styling and Colors
- Dial charts use custom fonts and colors
- Tables use color coding (red/yellow/green) based on performance thresholds
- Word visualizations use gradients and sentiment-based coloring

## Output

### PowerPoint Presentation
- Executive summary with dial charts
- Participation analysis by department/position
- Detailed breakdowns for each assessment category
- Word association analysis and comparisons
- Statistical tables with outlier highlighting

### Individual Reports (PDF)
- Personal performance dials
- Individual improvement areas
- Word association gradient analysis
- Customized recommendations

## Troubleshooting

### Common Issues
1. **File Path Errors**: Ensure directory structure matches expected paths
2. **Missing Dependencies**: Install all required packages
3. **Data Format Issues**: Verify CSV files have correct column names
4. **Memory Issues**: Large datasets may require processing in batches

### Performance Optimization
- Use batch processing for large user sets
- Enable multiprocessing for report generation
- Clear memory after processing large visualizations

## License

This project is proprietary software. All rights reserved.
