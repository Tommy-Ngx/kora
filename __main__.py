# main.py

import argparse
import pandas as pd
from utils import download_file_from_google_drive, Frax
from kora.selenium import wd as wd2
from tqdm import tqdm
from datetime import datetime
from google.colab import output as output2
import os

def parse_arguments():
    parser = argparse.ArgumentParser(description="Frax Crawling Script")
    parser.add_argument("--dataset-dir", required=True, help="Path to the CSV dataset file")
    parser.add_argument("--save-to", required=True, help="Path to save the output")
    parser.add_argument("--BMD-column", required=True, help="BMD column name")
    parser.add_argument("--task", required=True, choices=["BMD", "Tscore"], help="Specify the task (BMD or Tscore)")
    return parser.parse_args()

def main():
    args = parse_arguments()

    # Load CSV file using pandas
    FraxInput = pd.read_csv(args.dataset_dir)
    filtered_row_count1 = len(FraxInput)
    FraxInput = FraxInput[FraxInput[args.BMD_column].notnull()]
    FraxInput = FraxInput[FraxInput['AGE'] >= 40]
    FraxInput = FraxInput[(FraxInput['WGHT'] >= 25) & (FraxInput['WGHT'] <= 125)]
    output2.clear()
    # Print filtered row count
    filtered_row_count = len(FraxInput)
    print(f"Current row count: {filtered_row_count1}")
    print(f"Filtered row count: {filtered_row_count}")

    FraxResult = []

    # Your FraxInput DataFrame loop
    for index, row in tqdm(FraxInput.iterrows(), total=len(FraxInput), desc='', unit='row'):
        id1 = row['ID']
        gender1 = row['GENDER']
        age1 = row['AGE']
        weight1 = row['WGHT']
        height1 = row['HGHT']
        prefra1 = 0  # row['FX50']
        parent1 = 0  # row['ParentF']
        smoke1 = row['SMOKE']
        rheu1 = row['RHEUMATOID']
        seosteo1 = row['2OSTEO']
        drink1 = row['DRWK']
        corti1 = row['CORTICOID']
        nfall1 = row['NFALL']
        bmd1 = row[args.BMD_column]

        # Call the Frax function from utils
        #outputallthing = Frax(
        #    wd=wd2, id=id1, age=age1, gender=gender1, weight=weight1, height=height1,
        #    prefra=prefra1, nfall=nfall1, parent=parent1, smoke=smoke1,
        #    rheu=rheu1, seosteo=seosteo1 ,drink=drink1, corti=corti1, bmd=bmd1, folder=args.BMD_column
        #)

        # Call the Frax function from utils
        outputallthing = Frax(
            wd=wd2, id=id1, age=age1, gender=gender1, weight=weight1, height=height1,
            prefra=prefra1, nfall=nfall1, parent=parent1, smoke=smoke1, 
            rheu=rheu1, seosteo= seosteo1, drink=drink1, corti=corti1, bmd=bmd1, folder=args.BMD_column, task=args.task
        )

        # Update tqdm description with the relevant information
        if task == "BMD":
            tqdm.write("{}|{}|Age:{}|Tscore:{}|MR:{}|HR:{}".format(outputallthing[0],
                outputallthing[1], outputallthing[2], outputallthing[15], outputallthing[16], outputallthing[17]
            ))
        else:
            tqdm.write("{}|{}|Age:{}|Tscore:{}|MR:{}|HR:{}".format(outputallthing[0],
                outputallthing[1], outputallthing[2], outputallthing[15], outputallthing[15], outputallthing[16]
            ))

        # Update tqdm description with the relevant information

        #tqdm.set_postfix( ID=outputallthing[0], Age=outputallthing[2], Tscore=outputallthing[14],
        #    MR=outputallthing[15],HR=outputallthing[16])
        #tqdm.update()

        FraxResult.append(outputallthing)

        # Convert FraxResult to DataFrame
        df_FraxResult = pd.DataFrame(FraxResult)

        # Rename columns
        if task == "BMD":
            df_FraxResult.rename(columns={
                0: 'ID', 1: 'GENDER', 2: 'AGE', 3: 'WGHT', 4: 'HGHT', 5: 'FX50', 6: "NFALL", 7: 'ParentF',
                8: 'SMOKE', 9: 'RHEUMATOID', 10:"2OSTEO" , 11: 'DRINK', 12: 'CORTICOID', 13: args.BMD_column, 14: "DXA",
                15: f"Tscore_{args.BMD_column}", 16: f"MOsteo_{args.BMD_column}", 17: f"HipFrax_{args.BMD_column}"
            }, inplace=True)
        else:
            df_FraxResult.rename(columns={
            0: 'ID', 1: 'GENDER', 2: 'AGE', 3: 'WGHT', 4: 'HGHT', 5: 'FX50', 6: "NFALL", 7: 'ParentF',
            8: 'SMOKE', 9: 'RHEUMATOID', 10:"2OSTEO" , 11: 'DRINK', 12: 'CORTICOID', 13: args.BMD_column, 14: "DXA",
            15: f"MOsteo_{args.BMD_column}", 16: f"HipFrax_{args.BMD_column}"
            }, inplace=True)

        #df_FraxResult.rename(columns={
        #    0: 'ID', 1: 'GENDER', 2: 'AGE', 3: 'WGHT', 4: 'HGHT', 5: 'FX50', 6: "NFALL", 7: 'ParentF',
        #    8: 'SMOKE', 9: 'RHEUMATOID', 10:"2OSTEO" , 11: 'DRINK', 12: 'CORTICOID', 13: args.BMD_column, 14: "DXA",
        #    15: f"Tscore_{args.BMD_column}", 16: f"MOsteo_{args.BMD_column}", 17: f"HipFrax_{args.BMD_column}"
        #}, inplace=True)

        # Generate current date for the filename
        current_date = datetime.now().strftime("%d%b%Y")

        # Define the output CSV file path
        output_csv_path = f'{args.save_to}/FRAX_{args.BMD_column}_{current_date}.csv'

        # Check if the file already exists
        if os.path.isfile(output_csv_path):
            # Append to the existing file without writing header
            #df_FraxResult.to_csv(output_csv_path, mode='a', header=False, encoding='utf-8', index=False)
            df_FraxResult.to_csv(output_csv_path, encoding='utf-8', index=False)
        else:
            # Save as a new file with header
            df_FraxResult.to_csv(output_csv_path, encoding='utf-8', index=False)

    # Print the final DataFrame
    print(df_FraxResult)
    df_FraxResult.to_csv(output_csv_path, encoding='utf-8', index=False)

if __name__ == "__main__":
    main()
