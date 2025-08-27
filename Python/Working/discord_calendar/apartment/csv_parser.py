import gspread

gc = gspread.service_account()

spreadsheet_name = "Ledger Form (Responses)" 
spreadsheet = gc.open(spreadsheet_name)
csv_data_bytes = spreadsheet.export(format=gspread.utils.ExportFormat.CSV)
output_filename = f"{spreadsheet_name}.csv"

with open(output_filename, "wb") as f:
    f.write(csv_data_bytes)

file = open(output_filename)
table = []

row_list = file.read().split("\n")
for row in row_list:
    output_row = row.split()
    table.append(output_row)

def print_row(row_index):
    row = table[row_index]
    print(f"{row_index}: {row}")

def full_print():
    for i in range(len(table)):
        print_row(i)

def transaction_print(should_print=False):
    output = []
    for i in range(len(table)):
        if i != 0:
            transaction_list = table[i][1].split(",")
            sender = transaction_list[1]
            receiver = transaction_list[2]
            amount = float(transaction_list[3][1:])
            if should_print:
                print(f"{sender} -> {receiver} [${amount}]")
            output.append([sender, receiver, amount])
    print()
    return output


def tally_transactions():
    transaction_list = transaction_print()
    person_dict = {
        "Jon": 0,
        "Bee": 0,
        "Grace": 0,
        "Michael": 0
    }
    for transaction in transaction_list:
        try:
            person_dict[transaction[0]] -= transaction[2]
            person_dict[transaction[1]] += transaction[2]
        except:
            print(f"'{transaction[0]}' or '{transaction[1]}' are not valid names")
    for person in person_dict:
        person_dict[person] = round(person_dict[person], 2)
    output = ""
    for person in person_dict:
        print_statement = f"{person}: {person_dict[person]}"
        print(print_statement)
        output = output + print_statement + "\n"
    return output


if __name__ == "__main__":
    tally_transactions()