import pandas as pd
import sys

# -------------------------------------------------
# STEP 1: Load Orange Book Data Files
# -------------------------------------------------

def load_data():
    try:
        products = pd.read_csv("products.txt", sep="~", dtype=str)
        patents = pd.read_csv("patent.txt", sep="~", dtype=str)
        exclusivity = pd.read_csv("exclusivity.txt", sep="~", dtype=str)
    except Exception as e:
        print("Error loading Orange Book files:", e)
        sys.exit()

    return products, patents, exclusivity


# -------------------------------------------------
# STEP 2: Search Molecule (Exact to Your Columns)
# -------------------------------------------------

def search_molecule(molecule, products):
    molecule = molecule.lower()

    filtered = products[
        products["Ingredient"].str.lower().str.contains(molecule, na=False) |
        products["Trade_Name"].str.lower().str.contains(molecule, na=False)
    ]

    return filtered


# -------------------------------------------------
# STEP 3: Extract Patent & Exclusivity
# -------------------------------------------------

def get_patent_info(app_numbers, patents):
    return patents[patents["Appl_No"].isin(app_numbers)]


def get_exclusivity_info(app_numbers, exclusivity):
    return exclusivity[exclusivity["Appl_No"].isin(app_numbers)]


# -------------------------------------------------
# STEP 4: Query Engine
# -------------------------------------------------

def query_engine(product_df, patent_df, exclusivity_df, question):
    question = question.lower()

    if "applicant full" in question:
        return product_df["Applicant_Full_Name"].unique().tolist()

    if "applicant" in question:
        return product_df["Applicant"].unique().tolist()

    if "application" in question:
        return product_df["Appl_No"].unique().tolist()

    if "strength" in question:
        return product_df["Strength"].unique().tolist()

    if "dosage" in question or "route" in question:
        return product_df["DF;Route"].unique().tolist()

    if "approval" in question:
        return product_df["Approval_Date"].unique().tolist()

    if "te code" in question:
        return product_df["TE_Code"].unique().tolist()

    if "rld" in question:
        return product_df["RLD"].unique().tolist()

    if "patent" in question:
        return patent_df.to_dict(orient="records")

    if "exclusiv" in question:
        return exclusivity_df.to_dict(orient="records")

    if "all" in question:
        return {
            "Products": product_df.to_dict(orient="records"),
            "Patents": patent_df.to_dict(orient="records"),
            "Exclusivity": exclusivity_df.to_dict(orient="records")
        }

    return "Question not recognized."


# -------------------------------------------------
# MAIN EXECUTION
# -------------------------------------------------

def main():
    print("\nUS FDA ORANGE BOOK KNOWLEDGE MINER")
    print("-" * 50)

    products, patents, exclusivity = load_data()

    molecule = input("Enter drug name: ").strip()

    product_results = search_molecule(molecule, products)

    if product_results.empty:
        print("No results found.")
        sys.exit()

    app_numbers = product_results["Appl_No"].unique()

    patent_results = get_patent_info(app_numbers, patents)
    exclusivity_results = get_exclusivity_info(app_numbers, exclusivity)

    print("\nProduct Results:")
    print(product_results[[
        "Appl_No",
        "Trade_Name",
        "Applicant",
        "Ingredient",
        "DF;Route",
        "Strength",
        "TE_Code"
    ]])

    while True:
        question = input("\nAsk a question (or type 'exit'): ").strip()

        if question.lower() == "exit":
            print("Exiting.")
            break

        answer = query_engine(product_results, patent_results, exclusivity_results, question)
        print("\nAnswer:")
        print(answer)


if __name__ == "__main__":
    main()