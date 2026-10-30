
import pandas as pd

# ==========================================
# AI ACADEMIC PERFORMANCE REPORT GENERATOR
# ==========================================

# 1. Load student dataset
df = pd.read_csv("student_data.csv")

# 2. Define subjects and target
subjects = [
    "Math_Mastery",
    "Science_Mastery",
    "English_Mastery"
]

TARGET = 80

# 3. Calculate average mastery
df["Average_Mastery"] = (
    df[subjects].mean(axis=1).round(2)
)

# 4. Calculate academic progress
df["Progress"] = (
    df["Average_Mastery"] - df["Previous_Mastery"]
).round(2)

# 5. Calculate gap to target
df["Gap_To_Target"] = (
    TARGET - df["Average_Mastery"]
).clip(lower=0).round(2)


# 6. Assign support priority
def assign_priority(mastery):

    if mastery < 40:
        return "Urgent Support"
    elif mastery < 60:
        return "High Priority"
    elif mastery < 80:
        return "Monitor Progress"
    else:
        return "Target Achieved"


df["Priority"] = df["Average_Mastery"].apply(
    assign_priority
)


# 7. Detect learning trends
def detect_trend(progress):

    if progress < 0:
        return "Declining"
    elif progress > 0:
        return "Improving"
    else:
        return "No Change"


df["Learning_Trend"] = df["Progress"].apply(
    detect_trend
)


# 8. Identify academic risk
def identify_risk(row):

    if row["Average_Mastery"] < 40:
        return "Critical Risk"

    elif row["Average_Mastery"] < 60 and row["Progress"] < 0:
        return "High Risk"

    elif row["Average_Mastery"] < 60:
        return "Moderate Risk"

    elif row["Progress"] < 0:
        return "Monitor Closely"

    else:
        return "Low Risk"


df["Risk_Level"] = df.apply(
    identify_risk,
    axis=1
)


# 9. Display academic performance report
print("\n==========================================")
print("       ACADEMIC PERFORMANCE REPORT")
print("==========================================")

print(
    df[[
        "Student_Name",
        "Average_Mastery",
        "Progress",
        "Gap_To_Target",
        "Priority",
        "Learning_Trend",
        "Risk_Level"
    ]].to_string(index=False)
)


# 10. Identify declining students
declining_students = df[
    df["Learning_Trend"] == "Declining"
]

print("\n==========================================")
print("          DECLINING STUDENTS")
print("==========================================")

if not declining_students.empty:

    print(
        declining_students[[
            "Student_Name",
            "Progress",
            "Risk_Level"
        ]].to_string(index=False)
    )

else:
    print("No declining students detected.")


# 11. Identify high-risk students
high_risk_students = df[
    df["Risk_Level"].isin([
        "Critical Risk",
        "High Risk"
    ])
]

print("\n==========================================")
print("            HIGH-RISK STUDENTS")
print("==========================================")

if not high_risk_students.empty:

    print(
        high_risk_students[[
            "Student_Name",
            "Average_Mastery",
            "Progress",
            "Risk_Level"
        ]].to_string(index=False)
    )

else:
    print("No high-risk students detected.")


# 12. Generate class summary
print("\n==========================================")
print("              CLASS SUMMARY")
print("==========================================")

print("Total Students:", len(df))

print(
    "Class Average:",
    round(df["Average_Mastery"].mean(), 2)
)

print(
    "Students Needing Support:",
    (df["Average_Mastery"] < TARGET).sum()
)

print(
    "Students Declining:",
    len(declining_students)
)

print(
    "Students Improving:",
    (df["Learning_Trend"] == "Improving").sum()
)

print(
    "Students Achieving Target:",
    (df["Average_Mastery"] >= TARGET).sum()
)

print(
    "High/Critical Risk Students:",
    len(high_risk_students)
)

print("\n===== REPORT GENERATION COMPLETED =====")
