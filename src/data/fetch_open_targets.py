import requests
import pandas as pd
import json
import os

def fetch_nsclc_targets():
    """
    Fetches targets associated with Non-Small Cell Lung Carcinoma (NSCLC) 
    from the Open Targets GraphQL API.
    EFO ID for NSCLC is MONDO_0005233.
    """
    print("Fetching Target-Disease associations for NSCLC from Open Targets...")
    
    query = """
    query lungCancerTargets {
      disease(efoId: "MONDO_0005233") {
        id
        name
        associatedTargets(page: {index: 0, size: 500}) {
          count
          rows {
            target {
              id
              approvedSymbol
              approvedName
              proteinIds {
                id
                source
              }
            }
            score
            datatypeScores {
              id
              score
            }
          }
        }
      }
    }
    """
    
    url = "https://api.platform.opentargets.org/api/v4/graphql"
    response = requests.post(url, json={"query": query})
    
    if response.status_code == 200:
        data = response.json()
        if not data.get('data') or not data['data'].get('disease'):
            print("API returned unexpected data:")
            print(json.dumps(data, indent=2))
            return None
        
        targets = data['data']['disease']['associatedTargets']['rows']
        
        target_list = []
        for t in targets:
            target_info = t['target']
            uniprot_id = None
            if target_info.get('proteinIds'):
                for pid in target_info['proteinIds']:
                    if pid['source'] == 'uniprot':
                        uniprot_id = pid['id']
                        break
                        
            target_list.append({
                "disease_id": "MONDO_0005233",
                "disease_name": "Non-small cell lung carcinoma",
                "target_ensembl_id": target_info['id'],
                "target_symbol": target_info['approvedSymbol'],
                "target_name": target_info['approvedName'],
                "uniprot_id": uniprot_id,
                "association_score": t['score']
            })
            
        df = pd.DataFrame(target_list)
        
        # Save to raw data
        os.makedirs("../../data/raw", exist_ok=True)
        output_path = "../../data/raw/opentargets_nsclc_targets.csv"
        df.to_csv(output_path, index=False)
        print(f"Saved {len(df)} targets to {output_path}")
        return df
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return None

if __name__ == "__main__":
    fetch_nsclc_targets()
