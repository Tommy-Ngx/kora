# fix code 1 Dec 2023 for Tommy

import argparse
from utils import download_file_from_google_drive, findkeyinfo, Frax
from kora.selenium import wd as wd2
from tqdm import tqdm

def parse_arguments():
    parser = argparse.ArgumentParser(description="Frax Crawling Script")
    parser.add_argument("--dataset-dir", required=True, help="Path to the dataset directory")
    parser.add_argument("--save-to", required=True, help="Path to save the output")
    parser.add_argument("--BMD-column", required=True, help="BMD column name")
    return parser.parse_args()

def main():
    args = parse_arguments()

    # Your FraxInput DataFrame loading goes here
    # For example: FraxInput = pd.read_csv(args.dataset_dir)

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

    # Save or print FraxResult as needed
    #print(FraxResult)

if __name__ == "__main__":
    main()
