import os
import time
from datetime import datetime
import functions_framework
from google import genai

def get_previous_month_year():
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
    try:
        return client.interactions.get(name=interaction_id)
    except TypeError:
        try:
            return client.interactions.get(interaction_id=interaction_id)
        except TypeError:
            return client.interactions.get(interaction_id)

@functions_framework.http
def run_cti_research(request):
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
    
    interaction = client.interactions.create(
        agent='deep-research-preview-04-2026',
        input=prompt,
        background=True
    )
    
    print(f"Interaction registered with ID: {interaction.id}")
    
    active_statuses = ['in_progress', 'pending', 'queued', 'running']
    while interaction.status in active_statuses:
        time.sleep(20)
        interaction = fetch_interaction_state(client, interaction.id)
        
    print(f"Agent execution completed with status: {interaction.status}")
    
    if interaction.status in ['failed', 'error']:
        return f"Agent failed. Status: {interaction.status}", 500
        
    return interaction.output_text, 200