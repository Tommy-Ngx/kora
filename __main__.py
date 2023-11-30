# main.py

import argparse
import pandas as pd
from utils import download_file_from_google_drive, findkeyinfo, Frax
from kora.selenium import wd as wd2
from tqdm import tqdm
from datetime import datetime

def parse_arguments():
    parser = argparse.ArgumentParser(description="Frax Crawling Script")
    parser.add_argument("--dataset-dir", required=True, help="Path to the CSV dataset file")
    parser.add_argument("--save-to", required=True, help="Path to save the output")
    parser.add_argument("--BMD-column", required=True, help="BMD column name")
    return parser.parse_args()

def main():
    args = parse_arguments()

    # Load CSV file using pandas
    FraxInput = pd.read_csv(args.dataset_dir)

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
        drink1 = row['DRWK']
        corti1 = row['CORTICOID']
        nfall1 = row['NFALL']
        bmd1 = row[args.BMD_column]

        # Call the Frax function from utils
        outputallthing = Frax(
            wd=wd2, id=id1, age=age1, gender=gender1, weight=weight1, height=height1,
            prefra=prefra1, nfall=nfall1, parent=parent1, smoke=smoke1,
            rheu=rheu1, drink=drink1, corti=corti1, bmd=bmd1, folder=args.BMD_column
        )

        # Update tqdm description with the relevant information
        tqdm.write("{}|Age:{}|Tscore:{}|MR:{}|HR:{}".format(
            outputallthing[1], outputallthing[2], outputallthing[14], outputallthing[15], outputallthing[16]
        ))

        FraxResult.append(outputallthing)

    # Convert FraxResult to DataFrame
    df_FraxResult = pd.DataFrame(FraxResult)

    # Rename columns
    df_FraxResult.rename(columns={
        0: 'ID', 1: 'GENDER', 2: 'AGE', 3: 'WGHT', 4: 'HGHT', 5: 'FX50', 6: "NFALL", 7: 'ParentF',
        8: 'SMOKE', 9: 'RHEUMATOID', 10: 'DRINK', 11: 'CORTICOID', 12: args.BMD_column, 13: "DXA",
        14: f"Tscore_{args.BMD_column}", 15: f"MOsteo_{args.BMD_column}", 16: f"HipFrax_{args.BMD_column}"
    }, inplace=True)

    # Save the DataFrame to a CSV file
    current_date = datetime.now().strftime("%d%b%Y")
    output_csv_path = f'{args.save_to}/FRAX_{args.BMD_column}_{current_date}.csv'
    df_FraxResult.to_csv(output_csv_path, encoding='utf-8', index=False)


    # Print the DataFrame
    print(df_FraxResult)

if __name__ == "__main__":
    main()
