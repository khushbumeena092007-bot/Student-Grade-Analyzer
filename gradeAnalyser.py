import pandas as pd
import numpy as np
import os

def GradeAnalyser(file_path):


    df = pd.read_csv(file_path)      


    # handling  missing values
    df["Name"]= df["Name"].fillna("unknown")

    df["City"]= df["City"].fillna("unknown")

    df["Attendance_Percentage"]=pd.to_numeric(df["Attendance_Percentage"], errors="coerce")
    df["Attendance_Percentage"]= df["Attendance_Percentage"].clip(lower=0, upper=100)
    df["Attendance_Percentage"]= df["Attendance_Percentage"].fillna(df["Attendance_Percentage"].median())
    # print(df["Attendance_Percentage"].head(10))


    df["Gender"]=df["Gender"].str.strip().str.upper()
    df["Gender"]= df["Gender"].replace({
        "M": "Male",
        "F": "Female",
        "MALE": "Male",
        "FEMALE": "Female"
    })


    # Making a list of all subjects and clean and handle the missing data in this.
    subjects=[
        "Mathematics",
        "Science",
        "English",
        "Social_Studies",
        "Computer_Science",
        "Hindi"
        ]
    for subject in subjects:
        df[subject]= pd.to_numeric(df[subject] , errors = "coerce").round(2)

        df[subject]=df[subject].fillna(df[subject].mean()).round(2)


    # Calculating Average and Total marks and Add them as a new column in data.
    df["Average_marks"]=df[subjects].mean(axis=1).round(2)
    df["Total"]= df[subjects].sum(axis=1).round(2)

    # calculatin percentage 
    df["percentage"]=df["Average_marks"]

    # Assigne grades according to their marks
    def grade(p):
        if p>=90:
            return("A+")
        elif p>=80:
            return("A")
        elif p>=70:
            return("B")
        elif p>=60:
            return("C")
        elif p>=50:
            return("D")
        elif p>=40:
            return("E")
        else:
            return("F")
    # add Grade column
    df["Grade"]= df["percentage"].apply(grade)

    ##calculate and add Rank column
    df["Rank"]= df["percentage"].rank(ascending=False,method="min").astype(int)



    ##Add result column that shows student is pass or fail.
    df["Result"]= df["percentage"].apply( lambda x: "Pass" if x>=40 else "Fail")


    #adding a cloumn that shows class wise Rank.
    df["Class_Rank"]=df.groupby("Class")["percentage"].rank(ascending=False, method="min").astype(int)


    # CALCULATING SUBJECT WISE RANK, GRADE AND RESULT.
    for subject in subjects:
        df[subject+"_rank"] = df[subject].rank(ascending = False,method="min").astype(int)
        df[subject+"_Grade"]=df[subject].apply(grade)
        df[subject+"_Result"]=df[subject].apply( lambda x: "Pass" if x>=40 else "Fail")


    # Build a dictinary Demography
    Demography={

        "classwise_total_students" : df.groupby("Class")["Student_ID"].count(),
        "classwise_per_city_students": df.groupby("Class")["City"].value_counts(),
        "classwise_total_result": df.groupby("Class")["Result"].value_counts(),
        "citywise_total_students": df.groupby("City")["Student_ID"].count(),
        "citywise_total_result": df.groupby("City")["Result"].value_counts()
    }



    #class_summary(Class average in every subject)
    Class_Summary=df.groupby("Class")[subjects].mean().round(2)

    #Gender_summary
    Gender_Summary=df.groupby("Gender")[subjects].mean().round(2)

    #Class_Gender_summary
    Class_Gender_Summary=df.groupby(["Class","Gender"])[subjects].mean().round(2)

    #city and class-wise summary
    City_Class_Summary=df.groupby(["Class","City"])[subjects].mean().round(2)


    #top 10 students Data
    top_10=df.sort_values("Rank").head(10)
    # print(top_10)


    #BOttam 10 students Data
    bottam_10= df.sort_values("Rank").tail(10)


    # At risk students
    At_Risk= df[(df["percentage"]<50) &(df["Attendance_Percentage"]<75)]


    # failure rate subject wise
    failure_rate=pd.DataFrame({
        "subject":subjects,
        "Failure rate (%)":[round((df[sub]<40).mean()*100, 2) for sub in subjects]
    })


    ##store  data in excel files
    with pd.ExcelWriter("student_Grade_Reports.xlsx", engine="openpyxl" ) as writer:
        df.to_excel(
            writer,
            sheet_name="Students_Cleaned_Report",
            index=False
        )
        Class_Summary.to_excel(
            writer,
            sheet_name="Class_Summary"
        )
        Gender_Summary.to_excel(
            writer,
            sheet_name="Gender_Summary"
        )
        Class_Gender_Summary.to_excel(
            writer,
            sheet_name="Class_Gender_summary"
        )
        City_Class_Summary.to_excel(
            writer,
            sheet_name="City_Class_Summary"
        )
        top_10.to_excel(
            writer,
            sheet_name="Top_10_students",
            index=False
        )
        bottam_10.to_excel(
            writer,
            sheet_name="Bottam_10_Students",
            index=False
        )
        At_Risk.to_excel(
            writer,
            sheet_name="At_Risk",
            index=False
        )
        failure_rate.to_excel(
            writer,
            sheet_name="Failure_rate",
            index=False
        )
            
        #Add demography sheet
        for sheet_name , data in Demography.items():
            data.reset_index().to_excel(
                writer,
                sheet_name=sheet_name[:31],
                index=False
            )

    ##store  class-wise data in excelfiles
    with pd.ExcelWriter("Students_Classwise_Reports.xlsx",engine="openpyxl") as writer:
        #All students sheet
        df.to_excel(
            writer,
            sheet_name="All_Students",
            index=False
        )
        # Each class sheet
        for class_name , class_df in df.groupby("Class"):

            sheet=str(class_name)[:31]
            class_df.sort_values("Rank").to_excel(
                writer,
                sheet_name = sheet,
                index=False
            )



    import matplotlib
    import matplotlib.pyplot as plt
    import os
    
    os.makedirs("graphs", exist_ok=True)
    #Average marks
    Class_Summary["Avarage"]= Class_Summary.mean(axis=1)

    plt.bar(Class_Summary.index,Class_Summary["Avarage"])
    plt.title("class avarage summary")
    plt.xlabel("class"); plt.ylabel("Avarage marks")
    plt.tight_layout()
    plt.savefig("graphs/class_bar.png")
    plt.close()


    # subject wise Avarage bar chart
    subject_avg=df[subjects].mean()
    plt.figure(figsize=(8,5))
    plt.bar(subject_avg.index, subject_avg.values)
    plt.title("Subject Average chart")
    plt.xlabel("subjects")
    plt.ylabel("Averge marks")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig("graphs/subject_Average.png")
    plt.close()


    # pass vs fail students
    result=df["Result"].value_counts()
    plt.figure(figsize=(6,4))
    plt.bar(result.index, result.values)
    plt.title("Pass vs Fail students count")
    plt.xlabel("result"); plt.ylabel("values")
    plt.tight_layout()
    plt.savefig("graphs/result_bar.png")
    plt.close()


    # # attendance chart
    plt.figure(figsize=(8,5))
    plt.hist(df["Attendance_Percentage"], bins=10)
    plt.title("Attendance Chart")
    plt.xlabel("Attendance percentage")
    plt.ylabel("percentage(%)")
    plt.tight_layout()
    plt.savefig("graphs/Attendance_chart.png")
    plt.close()


    # gender distribution
    gender=df["Gender"].value_counts()
    plt.figure(figsize=(6,6))
    plt.pie(gender,
    labels=gender.index,
    autopct="%1.1f%%",
    startangle=90)
    plt.title("Gender Distribution")
    plt.tight_layout()
    plt.savefig("graphs/gender_distribution.png")
    plt.close()

    #class strenth
    classStrength=df["Class"].value_counts()
    plt.bar(
        classStrength.index,
        classStrength.values)
    plt.tight_layout()
    plt.title("Class Strength")
    plt.tight_layout()
    plt.savefig("graphs/Class_strength.png")
    plt.close()


    # aatendance vs percentage graph
    plt.figure(figsize=(8,5))
    plt.scatter(df["Attendance_Percentage"],df["percentage"])
    plt.title("Attendance vs percentage Graph")
    plt.tight_layout()
    plt.savefig("graphs/AttendanceVS_percentage.png")
    plt.close()
    return(df,Class_Summary,Gender_Summary,Class_Gender_Summary,City_Class_Summary,top_10,bottam_10,At_Risk,failure_rate,Demography)






