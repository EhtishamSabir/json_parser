import pandas as pd
import json
from message_reader import start

# setting up config file

input_file = "input.csv"
output_file = "out.csv"
json_file = "var_old.json"

# reading input file & sheet
df = pd.read_csv(input_file, header=None)
final_written = None


def to_every_message(row):
    global final_written
    cell_value = row[0]

    print(cell_value)

    # getting response from core function
    path_list, response_list = start(file_name=json_file)

    write_list = [(cell_value, "", "")]
    for new_row in zip(path_list, response_list):
        write_list.append(("send", "text", new_row[0]))
        write_list.append(("expectPayload", "equalTo", new_row[1]))
    if final_written is None:
        final_written = write_list
    else:
        final_written = final_written + write_list


# after reading each yellow lable applying function
df.apply(to_every_message, raw=True, axis=1)

# from dataframes to output excel
df_out = pd.DataFrame(final_written)
df_out.to_csv(output_file, index=False, header=False,encoding='Windows-1252')
