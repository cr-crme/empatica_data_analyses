import empatica as emp
from matplotlib import pyplot as plt

data_path_folder = (
    "C:\\Users\\pariterre\\Nextcloud\\Documents\\Technopole\\Projets\\DanielleLevac\\Empatica data\\Data\\"
)
# subjects = [
#     emp.Subject("01", ["2022-06-28", "2022-06-30", "2022-07-06", "2022-07-08"], data_path_folder),
#     emp.Subject("02", ["2022-07-04", "2022-07-05", "2022-07-06"], data_path_folder),
#     emp.Subject("03", ["2022-06-27", "2022-06-29", "2022-07-05", "2022-07-07"], data_path_folder),
#     emp.Subject("04", ["2022-06-29", "2022-07-07", "2022-07-08"], data_path_folder),
#     emp.Subject("05", ["2022-06-27", "2022-07-01"], data_path_folder),
#     emp.Subject("06", ["2022-06-30", "2022-07-04"], data_path_folder),
# ]
subjects = [
    emp.Subject("01", ["2022-06-28"], data_path_folder),
]


def main():
    for subject in subjects:
        # subject.plot(emp.DataType.EDA)
        subject.plot(emp.DataType.HR)

    plt.show()


if __name__ == "__main__":
    main()
