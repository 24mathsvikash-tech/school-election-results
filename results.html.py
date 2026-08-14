import os
import pandas as pd

def find_data_file():
    """Locates the downloaded Google Form responses file."""
    files = os.listdir('.')
    for f in files:
        if (f.endswith('.xlsx') or f.endswith('.csv')) and 'voter' not in f.lower():
            return f
    return None

def calculate_election_results():
    data_file = find_data_file()
    
    if not data_file:
        print("ERROR: No response file found in this folder!")
        return

    print(f"Reading file: {data_file}\n")

    if data_file.endswith('.csv'):
        df = pd.read_csv(data_file)
    else:
        df = pd.read_excel(data_file)

    # Clean up column names (strip extra spaces)
    df.columns = [str(col).strip() for col in df.columns]

    # 1. General Posts Tally
    print("==================================================")
    print("           1. GENERAL POSTS VOTE TALLY            ")
    print("==================================================")
    for post in ['School Captain', 'Vice School Captain', 'Sports Captain']:
        # Match column flexibly
        matched_cols = [c for c in df.columns if post.lower() in c.lower()]
        for col in matched_cols:
            print(f"\n--- {col.upper()} ---")
            counts = df[col].value_counts().dropna()
            for candidate, votes in counts.items():
                print(f"  • {candidate}: {votes} votes")

    # 2. House Captains Tally
    print("\n==================================================")
    print("        2. HOUSE CAPTAINS VOTE TALLY              ")
    print("==================================================")
    
    # Identify all columns related to House Captains
    house_captain_cols = [c for c in df.columns if 'house captain' in c.lower()]
    
    house_votes = []

    for _, row in df.iterrows():
        voter_id = row.get('Voter ID', 'Unknown')
        voter_house = row.get('House', 'General')

        for col in house_captain_cols:
            val = row.get(col)
            if pd.notna(val) and str(val).strip() != '':
                # Determine house name from column name or 'House' column
                col_lower = col.lower()
                if 'blue' in col_lower:
                    h_name = 'Blue'
                elif 'green' in col_lower:
                    h_name = 'Green'
                elif 'red' in col_lower:
                    h_name = 'Red'
                elif 'yellow' in col_lower:
                    h_name = 'Yellow'
                else:
                    h_name = voter_house

                house_votes.append({
                    'Voter_ID': voter_id,
                    'House': h_name,
                    'Candidate': str(val).strip()
                })

    votes_df = pd.DataFrame(house_votes)
    
    if not votes_df.empty:
        results = votes_df.groupby(['House', 'Candidate']).size().reset_index(name='Total_Votes')
        results = results.sort_values(by=['House', 'Total_Votes'], ascending=[True, False])
        
        for house, group in results.groupby('House'):
            print(f"\n--- {str(house).upper()} HOUSE CAPTAIN ---")
            for _, r in group.iterrows():
                print(f"  • {r['Candidate']}: {r['Total_Votes']} votes")
    else:
        print("No house captain votes recorded yet.")

if __name__ == "__main__":
    calculate_election_results()