# xr-education-cross-disciplinary-teams
Replication materials for cross-disciplinary XR education study
# Cross-Disciplinary XR Education: Team Formation Study

License: MIT (see `LICENSE`)

**Replication materials for:** *Cross-Disciplinary vs Same-Branch Team Formation in Progressive XR Engineering Education: Effects on Learning Outcomes and Collaborative Experience*

**Authors:** Sunny Nanade, Koteswara Rao Anne  
**Affiliation:** NMIMS Mukesh Patel School of Technology Management & Engineering, Mumbai, India  
**Status:** Manuscript under review at Frontiers in Education (submitted December 2025)

---

## Overview

This repository provides replication materials for a quasi-experimental study comparing cross-disciplinary and same-branch team formation in an AR/VR engineering course.

**Sample:** 60 undergraduate students from 9 engineering programmes  
**Design:** 14 teams (7 cross-disciplinary, 7 same-branch)  
**Duration:** 15-week semester  
**Hardware:** 5 Oculus Quest 2 headsets  
**Platform:** Unity game engine

### Key Findings

| Outcome | Effect Size | Significance | Interpretation |
|---------|-------------|--------------|----------------|
| Learning gains | d = 0.67 | p = .013 | Medium to large advantage for cross-disciplinary teams |
| Cross-learning experience | d = 1.86 | p < .001 | Very large effect favoring cross-disciplinary teams |
| Project quality | d = 1.01 | p = .084 | Trend toward higher scores (approaching significance) |

---

## Repository Structure

```
xr-education-cross-disciplinary-teams/
├── README.md                          # This file
├── LICENSE                            # MIT License
├── requirements.txt                   # Python dependencies
│
├── data/                              # Anonymized datasets
│   ├── students.csv                   # Student demographics & team assignments
│   ├── pretest_scores.csv             # Pre/post knowledge test scores
│   ├── project_rubric.csv             # Final project evaluations
│   └── collaboration_survey.csv       # Collaboration experience survey
│
├── code/                              # Analysis pipeline
│   ├── assign_teams.py                # Team formation algorithm
│   └── analyze_data.py                # Complete statistical analysis
│
├── instruments/                       # Assessment tools
│   ├── prepost_test.yaml              # 10-question knowledge test
│   ├── project_rubric.yaml            # 5-criterion project rubric
│   └── collaboration_survey.yaml      # 5-item Likert survey
│
├── results/                           # Publication-ready outputs
│   ├── tables/                        # CSV + LaTeX tables
│   │   ├── table1_learning_outcomes.*
│   │   ├── table2_project_quality.*
│   │   └── table3_collaboration.*
│   └── figures/                       # High-resolution figures (300dpi PNG)
│       ├── figure1_learning_gains.png
│       ├── figure2_project_scores.png
│       └── figure3_collaboration_radar.png
│
└── docs/                              # Documentation
    ├── REPLICATION_GUIDE.md           # Step-by-step replication instructions
    ├── REQUIRED_STATEMENTS.md         # Ethics, funding, author contributions
    └── references.bib                 # Complete bibliography with DOIs
```

---

## Quick Start

### Reproduce All Results

```bash
# 1. Clone repository
git clone https://github.com/sunny-nanade/xr-education-cross-disciplinary-teams.git
cd xr-education-cross-disciplinary-teams

# 2. Install dependencies (Python 3.10+)
pip install -r requirements.txt

# 3. Run complete analysis on real student data
python code/analyze_data.py

# 4. View results
# - Tables: results/tables/
# - Figures: results/figures/
# - Statistics: results/*.csv and results/reliability.txt
```

Expected outputs:
- Three publication-ready tables (CSV and LaTeX)
- Three figures (PNG, 300 dpi)
- Descriptive statistics, t-tests, effect sizes, and reliability (Cronbach's α ≈ .72)

---

## Results Summary

### Learning Outcomes

Cross-disciplinary teams showed significantly higher learning gains:
- Cross-disciplinary: *M* = 4.57 (*SD* = 1.63, *n* = 30)
- Same-branch: *M* = 3.61 (*SD* = 1.17, *n* = 28)
- *t*(56) = 2.54, *p* = .013, Cohen's *d* = 0.67

### Collaborative Learning Experience

Cross-disciplinary teams reported substantially higher collaboration quality:
- Cross-disciplinary: *M* = 4.42 (*SD* = 0.67, *n* = 31)
- Same-branch: *M* = 3.11 (*SD* = 0.74, *n* = 28)
- *t*(57) = 7.15, *p* < .001, Cohen's *d* = 1.86

### Project Quality

Cross-disciplinary teams showed higher overall project quality:
- Cross-disciplinary: *M* = 34.14 (*SD* = 5.24, *n* = 7 teams)
- Same-branch: *M* = 28.43 (*SD* = 6.08, *n* = 7 teams)
- *t*(12) = 1.85, *p* = .084, Cohen's *d* = 1.01

---

## Pedagogical Context

### Course Design

**Progressive curriculum:**
1. **Weeks 1-4:** Unity fundamentals (3D transforms, scripting basics)
2. **Weeks 5-8:** AR development (image tracking, plane detection)
3. **Weeks 9-11:** VR interactions (locomotion, object manipulation)
4. **Weeks 12-15:** Collaborative final project

**Peer-assisted learning:**
- Rotating expert roles (each student teaches one topic)
- 2-hour lab sessions with 5 Oculus Quest 2 headsets
- Hardware rotation system (all students get hands-on time)

### Theoretical Framework

- **Sociocultural learning** (Vygotsky, 1978)
- **Situated cognition** (Lave & Wenger, 1991)
- **Cognitive apprenticeship** (Brown et al., 1989)
- **Peer learning benefits** (Roscoe & Chi, 2007)

### Participants

- **N** = 60 undergraduate engineering students
- **Age:** *M* = 19.8 years (*SD* = 0.9), Range: 18-22
- **Gender:** 67% male (*n* = 40), 33% female (*n* = 20)
- **Branches:** Computer Science, Information Technology, Data Science, Artificial Intelligence, Cyber Security, Electronics & Telecommunication, Mechanical Engineering, MBA Tech (Computer), MBA Tech (AI)
- **Prior XR experience:** 12% (*n* = 7)

---

## Adaptation for Your Context

### Replication for Your Context

**Team formation algorithm (`code/assign_teams.py`):**

The algorithm operates in two stages:
1. Students are mapped to one of three disciplinary clusters based on their programme: Computing (CS, IT, Data Science), AI and Security (AI, Cyber Security), or Traditional Engineering (Electronics, Mechanical, and related branches).
2. A greedy iterative procedure forms cross-disciplinary teams by selecting students across clusters so that each team contains members from at least two distinct clusters, optimising for maximum cluster diversity while keeping team sizes between 4 and 5. Remaining students are assigned to same-branch teams drawn exclusively from within a single cluster (uniform size of 4).

```python
python code/assign_teams.py --input your_students.csv --output your_teams.csv
```

**Use our instruments:**
All assessment tools provided in `instruments/` folder (YAML format):
- Pre/post knowledge test (10 questions)
- Project evaluation rubric (5 criteria)
- Collaboration survey (5 Likert items, α = .72)

**Collect your data → Run analysis:**
```python
python code/analyze_data.py
```

---

## Citation

### Paper (APA 7th)

```
Nanade, S., & Anne, K. R. (2025). Cross-disciplinary vs same-branch team formation 
in progressive XR engineering education: Effects on learning outcomes and 
collaborative experience. Frontiers in Education (submitted December 2025).
```

### Data/Code Repository (APA 7th)

```
Nanade, S., & Anne, K. R. (2025). Cross-disciplinary XR education: Team formation 
study [Data set and code]. GitHub. 
https://github.com/sunny-nanade/xr-education-cross-disciplinary-teams
```

---

## License

**MIT License** - See [LICENSE](LICENSE) file for details.

You are free to:
- Use for any purpose (including commercial)
- Modify and redistribute
- Include in proprietary software

**Requirements:**
- Include copyright notice and license
- Cite our paper when using materials

---

## Contact

**Corresponding Author:**  
Sunny Nanade  
NMIMS Mukesh Patel School of Technology Management & Engineering  
Mumbai, India  
Email: sunny.nanade@nmims.edu

**Questions about:**
- **Data/Code:** sunny.nanade@nmims.edu
- **Pedagogical implementation:** sunny.nanade@nmims.edu
- **Institutional context:** Prof. Koteswara Rao Anne (Dean, MPSTME)

---

## Acknowledgments

We thank:
- The 60 undergraduate students who participated in this study
- Teaching assistants who supported laboratory sessions
- NMIMS MPSTME for institutional support and XR hardware
- Technical support team for maintaining Oculus Quest 2 devices

---

## Related Publications

- **Conference version:** Extended abstract presented at iCiTeL-2.0 (2024)
- **Full paper:** Submitted to Frontiers in Education (2025)

---

## Quick Links

- Paper status: Under review at Frontiers in Education (submitted December 2025)
- Journal: https://www.frontiersin.org/journals/education
- Issues/Questions: https://github.com/sunny-nanade/xr-education-cross-disciplinary-teams/issues

---

<!-- Repository statistics section removed to maintain academic presentation -->

---

**Version:** 1.1  
**Last Updated:** April 2026 (revised per reviewer feedback)  
**Status:** Manuscript under review, data publicly available

---

**For detailed replication instructions, see [`docs/REPLICATION_GUIDE.md`](docs/REPLICATION_GUIDE.md)**
