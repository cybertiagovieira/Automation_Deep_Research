import os
import time
from datetime import datetime
from google import genai

def get_previous_month_year():
    """Dynamically calculates the previous month and its corresponding year."""
    now = datetime.now()
    if now.month == 1:
        prev_month = 12
        prev_year = now.year - 1
    else:
        prev_month = now.month - 1
        prev_year = now.year
        
    dt = datetime(prev_year, prev_month, 1)
    return dt.strftime("%B, %Y")

def fetch_interaction_state(client, interaction_id):
    """Attempts to fetch interaction state using various expected parameter signatures."""
    try:
        return client.interactions.get(name=interaction_id)
    except TypeError:
        try:
            return client.interactions.get(interaction_id=interaction_id)
        except TypeError:
            return client.interactions.get(interaction_id)

def execute_monthly_cti_research():
    month_year_string = get_previous_month_year()
    
    prompt = f"""Execute a multi-stage deep research protocol for cyber threat intelligence (CTI) covering {month_year_string}.

    SEARCH CONSTRAINTS:
    - Prioritize primary intelligence sources: Mandiant, CrowdStrike, Microsoft Threat Intelligence, SentinelOne, CISA, and FS-ISAC reports.
    - Exclude: Consumer-level scams, basic retail fraud, website defacements, and low-impact DDoS events.
    - Focus exclusively on: Banking, Financial Services, Fintech, and systemic critical infrastructure.

    RESEARCH THRESHOLDS:
    You must iterate your search queries until you have definitively identified and extracted data for:
    1. A minimum of 4 distinct Apex Threat Actors (nation-state APTs or major ransomware syndicates) active in {month_year_string}.
    2. A minimum of 5 distinct high-impact incidents or breaches affecting the target sectors.
    3. At least 2 novel TTPs (Tactics, Techniques, and Procedures) involving cloud infrastructure, identity abuse, or zero-day exploitation.

    OUTPUT SCHEMA:
    Format the final report strictly using the following Markdown structure. Do not deviate or add extraneous sections.

    # Global CTI Report: {month_year_string}

    ## 1. Apex Threat Actors
    [Detail the actors, aliases, origins, and primary targets]

    ## 2. Notable Incidents and Breaches
    [Detail the incidents, compromised entities, and operational impacts]

    ## 3. TTP Evolution and Tooling
    [Detail the novel TTPs, specific CVEs exploited, and attack vectors]

    ## 4. Strategic Risk to Financial Ecosystems
    [Synthesize the macro-level systemic risks and defensive imperatives]
    """
    client = genai.Client()

    print(f"Starting Deep Research via SDK Interactions API for: {month_year_string}...")
    
    # 1. Create Long-Running Interaction
    interaction = client.interactions.create(
        agent='deep-research-preview-04-2026',
        input=prompt,
        background=True
    )
    
    print(f"Interaction registered with ID: {interaction.id}")
    print("Waiting for the Deep Research agent to complete (this process may take several minutes)...")

    # 2. Polling loop based on the status attribute
    active_statuses = ['in_progress', 'pending', 'queued', 'running']
    while interaction.status in active_statuses:
        time.sleep(20)
        print(".", end="", flush=True)
        interaction = fetch_interaction_state(client, interaction.id)
        
    print(f"\nAgent execution completed with status: {interaction.status}")
    
    # 3. Extract the final text report content
    if interaction.status in ['failed', 'error']:
        raise Exception(f"Agent failed. Status: {interaction.status}")
        
    return interaction.output_text

if __name__ == "__main__":
    # Ensure this environment variable is set with your actual AI Studio API key
    os.environ["GEMINI_API_KEY"] = "AIzaSyCluwq42XVpVyy-GP8iei6OHyEE0IoP34I"
    
    try:
        result = execute_monthly_cti_research()
        
        # Define dynamic filename based on the target month
        target_month_str = get_previous_month_year().replace(", ", "_")
        output_filename = f"CTI_Report_{target_month_str}.txt"
        
        # Write output to local text file
        with open(output_filename, "w", encoding="utf-8") as file:
            file.write(result)
            
        print(f"\n--- Report Generated Successfully and Saved as '{output_filename}' ---\n")
        
    except Exception as e:
        print(f"\nPipeline Failure: {e}")