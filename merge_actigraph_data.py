from enum import Enum
import csv


class FolderSuffixe(Enum):
    CAMP = "ActiGraph_CAMP"
    TOTAL = "ActiGraph_DailyDetailed"
    VR = "ActiGraph_VR"


data_path_folder = (
    "/home/pariterre/Documents/Documents/Technopole/Projets/DanielleLevac/Empatica data/Data/Actigraph"
)
trials = {
    "01": ["2022-06-28", "2022-06-30", "2022-07-04", "2022-07-06", "2022-07-08"],
    "02": ["2022-06-30", "2022-07-04", "2022-07-05", "2022-07-06", "2022-07-08"],
    "03": ["2022-06-27", "2022-06-29", "2022-07-05", "2022-07-07"],
    "04": ["2022-06-27", "2022-06-29", "2022-07-01", "2022-07-07", "2022-07-08"],
    "05": ["2022-06-27", "2022-06-29", "2022-07-01"],
    "06": ["2022-06-28", "2022-06-30", "2022-07-04", "2022-07-06", "2022-07-07"]
}

output_header = [
    "Subject",
    "Date",
    "Type",
    "METs",
    "% in Sedentary",
    "% in Light",
    "% in Moderate",
    "% in Vigorous",
    "Total MVPA",
    "% in MVPA",
    "Average MVPA Per Hour",
    "Steps Counts",
    "Steps Average Counts",
    "Steps Max Counts",
    "Steps Per Minute"
]
output_filename = "actigraph_compile_out.csv"


def main():
    # Note that data from 01_2022-06-30_ActiGraph_CAMP were collected on a french computer and were manually anglicised
    data_out = []
    for subject, dates in trials.items():
        for date in dates:
            for folder in FolderSuffixe:
                filepath = f"{data_path_folder}/{folder.name}/{subject}_{date}_{folder.value}.csv"

                with open(filepath, 'r', newline='') as csvfile:
                    rows = csv.reader(csvfile)

                    column_mapping = []
                    for i, row in enumerate(rows):
                        if i == 0:
                            for val in output_header:
                                column_mapping.append(None if val == "Type" else row.index(val))
                            continue

                        if i >= 2:
                            raise RuntimeError(
                                "This script is supposed to be used with CSV that has a header and one row of data"
                            )

                        data_tp = []
                        for j, val in enumerate(output_header):
                            if val == "Type":
                                data_tp.append(folder.name)
                            else:
                                data_tp.append(row[column_mapping[j]])
                        data_out.append(data_tp)

    with open(output_filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(output_header)
        for data in data_out:
            csvwriter.writerow(data)


if __name__ == "__main__":
    main()
