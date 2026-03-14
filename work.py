import json

# ==========================================
# 1. POLICY MODEL (The Rules)
# ==========================================
# This defines what is allowed and what is strictly forbidden.
SYSTEM_POLICY = {
    "allowed_actions": ["read_file", "list_directory"],
    "blocked_directories": ["/etc", "/system", "/root"],
    "allowed_directories": ["/var/log", "/tmp"]
}

# ==========================================
# 2. OPENCLAW: REASONING ENGINE (The Brain)
# ==========================================
class OpenClawAgent:
    def __init__(self):
        self.name = "SysAdmin-Agent"

    def reason_and_plan(self, user_prompt):
        """
        Mock reasoning: In a real app, an LLM would parse the prompt 
        and output a structured intent JSON.
        """
        print(f"[{self.name}] Thinking about: '{user_prompt}'")
        
        # Hardcoding the mock LLM outputs for demonstration
        if "read the logs" in user_prompt.lower():
            return {"intent_action": "read_file", "target_path": "/var/log/server.log"}
        elif "delete the system config" in user_prompt.lower():
            return {"intent_action": "delete_file", "target_path": "/etc/config.yaml"}
        else:
            return {"intent_action": "unknown", "target_path": ""}

# ==========================================
# 3. ARMORCLAW: ENFORCEMENT LAYER (The Bouncer)
# ==========================================
class ArmorClawValidator:
    def __init__(self, policy):
        self.policy = policy

    def validate_intent(self, intent_plan):
        """
        Checks the structured intent against the policy model BEFORE execution.
        """
        action = intent_plan.get("intent_action")
        target = intent_plan.get("target_path")

        print(f"[ArmorClaw] Validating Intent: Action='{action}', Target='{target}'")

        # Check 1: Is the action explicitly allowed?
        if action not in self.policy["allowed_actions"]:
            return False, f"Action '{action}' is not in the allowed actions list."

        # Check 2: Is the target in a blocked directory?
        for blocked_dir in self.policy["blocked_directories"]:
            if target.startswith(blocked_dir):
                return False, f"Target path '{target}' is in a protected directory."

        return True, "Intent complies with all system policies."

# ==========================================
# 4. EXECUTION LAYER (The Hands)
# ==========================================
class ExecutionSandbox:
    def execute(self, intent_plan):
        """
        The actual system execution (mocked here).
        """
        print(f"[Executor] SUCCESS: Executed {intent_plan['intent_action']} on {intent_plan['target_path']}\n")


# ==========================================
# 5. THE MAIN HACKATHON DEMO FLOW
# ==========================================
def run_system(user_prompt):
    print("-" * 50)
    print(f"USER: {user_prompt}")
    
    agent = OpenClawAgent()
    validator = ArmorClawValidator(SYSTEM_POLICY)
    executor = ExecutionSandbox()

    # Step 1: Reasoning
    plan = agent.reason_and_plan(user_prompt)

    # Step 2: Enforcement (Crucial Hackathon Requirement)
    is_valid, reason = validator.validate_intent(plan)

    # Step 3: Execution or Blocking
    if is_valid:
        print(f"[System] ALLOWED: {reason}")
        executor.execute(plan)
    else:
        print(f"[System] BLOCKED: {reason}")
        print("[Executor] Action aborted. System remains safe.\n")

# --- Run the Demo ---
if __name__ == "__main__":
    # Demo 1: An allowed action
    run_system("Can you read the logs for me?")
    
    # Demo 2: A blocked action (This proves your agent is safe)
    run_system("Delete the system config files to clean up space.")