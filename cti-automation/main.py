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
    
    prompt = f"""Conduct a comprehensive search for cyber threat intelligence (CTI) reports, threat landscape summaries, and cybersecurity news published in {month_year_string}. Focus on identifying the most active, dangerous, or newly emerging Threat Actors (including nation-state APTs, ransomware syndicates, and eCrime groups) operating in the global context, with a specific emphasis on those directly impacting the Banking, Financial Services, and Fintech sectors. Please extract and synthesize data detailing:
Apex Threat Actors: The names and aliases of the dominant threat actors active during this month.
Notable Incidents: Major cyberattacks, data breaches, systemic supply-chain compromises, or ransomware events they executed against financial institutions or global critical infrastructure.
TTP Evolution & Tooling: Shifts in their Tactics, Techniques, and Procedures (TTPs), including the use of new malware families, exploitation of specific vulnerabilities (CVEs), identity-based access methods, or novel evasion techniques (e.g., non-standard runtimes or cloud infrastructure abuse).
Motivations & Sector Impact: The underlying drivers for these campaigns (e.g., 'data-only' extortion, geopolitical pre-positioning, financial theft) and the resulting technical, operational, and systemic risks to the financial ecosystem."""

    client = genai.Client()

    print(f"Starting Deep Research via SDK Interactions API for: {month_year_string}...")
    
    # 1. Create Long-Running Interaction via the SDK native method
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
    os.environ["GEMINI_API_KEY"] = "AIzaSyCluwq42XVpVyy-GP8iei6OHyEE0IoP34I"
    
    try:
        result = execute_monthly_cti_research()
        print("\n--- Report Generated Successfully ---\n")
        print(result)
    except Exception as e:
        print(f"\nPipeline Failure: {e}")