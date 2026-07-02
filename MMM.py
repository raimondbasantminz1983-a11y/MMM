# =====================================================================
# COPYRIGHT NOTICE & LEGAL PROTECTION BLOCK
# Copyright (c) 2026 Raimond Basant Minz. All Rights Reserved.
# Protected under International Prior Art Guidelines.
# =====================================================================

import time
import re
import os
from datetime import datetime
from collections import deque

class MMM:
    def __init__(self, max_logs=200, max_input=5000, threshold=5, step_delay=0.3, intensity_mode=False):
        self.start_time = datetime.now()
        
        self.max_logs = max(1, max_logs)
        self.max_input = max(10, max_input)
        self.threshold = max(0, threshold)
        self.step_delay = max(0.0, step_delay)
        self.intensity_mode = intensity_mode
        
        self.state = "IDLE"
        self.risk_rules = {"override": 4, "bypass": 4, "harm": 5, "exploit": 5, "hack": 5}
        self.logs = deque(maxlen=self.max_logs)
        
        # MMM Unified Command Registry
        self.command_registry = {
            "state": {"func": lambda: print(f"Current State: {self.state}"), "desc": "View current system state parameters"},
            "logs": {"func": self.show_logs, "desc": "View live historic logs summary (Sequential)"},
            "clear": {"func": self.clear_screen, "desc": "Cross-platform terminal screen refresh"},
            "rules": {"func": self.show_rules, "desc": "View active threat matrix weights (Sorted)"},
            "threshold": {"func": self.show_threshold, "desc": "View core safety limit parameters"},
            "stats": {"func": self.show_stats, "desc": "View system telemetry dashboard metrics & uptime"},
            "help": {"func": self.show_help, "desc": "Auto-generate this runtime documentation menu"},
            "exit": {"func": None, "desc": "Safe and structured shutdown of framework execution"}
        }
        
        self.log("SYSTEM", "MMM Core Initialized and Armed")

    def log(self, stage, message):
        entry = {"time": datetime.now().strftime("%H:%M:%S"), "stage": stage, "message": message}
        self.logs.append(entry)
        print(f"[{entry['time']}] {stage} → {message}")

    def set_state(self, new_state):
        self.state = new_state
        self.log("STATE", f"Changed to {new_state}")

    def evaluate_input(self, text):
        score = 0
        matched = []
        words = re.findall(r'\b\w+\b', text.lower())
        target_tokens = words if self.intensity_mode else list(dict.fromkeys(words))
        
        for clean in target_tokens:
            if clean in self.risk_rules:
                score += self.risk_rules[clean]
                matched.append(clean)
                
        return score, list(dict.fromkeys(matched))

    def run_cycle(self, trigger_input):
        print("\n==============================")
        if len(trigger_input) > self.max_input:
            self.log("SECURITY", f"Rejected: Input length exceeds {self.max_input} limit.")
            return {"status": "REJECTED", "reason": "Input length violation"}
            
        try:
            self.set_state("AIR-PRESS")
            self.log("INPUT", trigger_input)
            time.sleep(self.step_delay)
            
            self.set_state("IGNITE")
            self.log("SCAN", "Analyzing intent...")
            score, unique_matched = self.evaluate_input(trigger_input)
            
            if score >= self.threshold:
                self.set_state("HALTED")
                return {
                    "status": "BLOCKED",
                    "risk_score": score,
                    "matched_terms": unique_matched,
                    "reason": "Risk threshold exceeded"
                }
                
            time.sleep(self.step_delay)
            self.set_state("EXECUTE")
            self.log("EXECUTION", "Validated route selected")
            time.sleep(self.step_delay)
            
            self.set_state("RESULT")
            return {
                "status": "SUCCESS",
                "risk_score": score,
                "matched_terms": unique_matched,
                "output": "Validated and Processed"
            }
        except Exception as e:
            self.log("ERROR", f"System anomaly caught: {str(e)}")
            return {"status": "ERROR", "reason": str(e)}
        finally:
            if self.state != "IDLE":
                self.set_state("IDLE")

    def show_logs(self):
        print("\n==== SYSTEM LOGS HISTORIC SPECIFICATION ====")
        if not self.logs:
            print("No logs recorded.")
            return
        for i, item in enumerate(self.logs, start=1):
            print(f"{i:03d} | {item['time']} | {item['stage']:<9} | {item['message']}")

    def summarize(self, result): 
        print("\n==== RESULT ====") 
        for k, v in result.items(): 
            print(f"{k}: {v}")

    def show_rules(self):
        print("\n==== ACTIVE RISK WEIGHTS (ALPHABETICAL SORT) ====")
        for k, v in sorted(self.risk_rules.items()):
            print(f"Keyword: {k:<10} | Weight: {v}")

    def show_threshold(self):
        print(f"\nCore Risk Threshold Limit: {self.threshold}")

    def clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")
        print("--- MMM Console Cleared ---")

    def show_stats(self):
        uptime = datetime.now() - self.start_time
        print("\n==== MMM TELEMETRY STATS & HEALTH SPECIFICATION ====")
        print(f"Current State      : {self.state}")
        print(f"Total Cached Logs  : {len(self.logs)} / {self.max_logs}")
        print(f"Core Risk Threshold: {self.threshold}")
        print(f"Active Logic Rules : {len(self.risk_rules)} keys loaded")
        print(f"Step Processing Lag: {self.step_delay}s")
        print(f"Scoring Mode Metric: {'Intensity/Repeated' if self.intensity_mode else 'Unique Signatures Only'}")
        print(f"System Live Uptime : {uptime.total_seconds():.2f} seconds")

    def show_help(self):
        print("\n--- MMM Command Guide (Unified Autogen Menu) ---")
        for cmd, meta in sorted(self.command_registry.items()):
            print(f"{cmd:<10} : {meta['desc']}")


if __name__ == "__main__":
    rbm = MMM()  # Initializing MMM Object
    print("\n--- MMM Enterprise Live Console Ready ---")
    print("Type 'help' to review the centrally unified command architecture.")
    
    while True:
        user_input = input("\nEnter prompt/command to test in MMM: ").strip()
        if not user_input:
            continue
            
        cmd = user_input.lower()
        if cmd == 'exit':
            print("Shutting down MMM safely...")
            rbm.show_logs()
            break
            
        if cmd in rbm.command_registry:
            execution_target = rbm.command_registry[cmd]["func"]
            if execution_target:
                execution_target()
        else:
            raw_result = rbm.run_cycle(user_input)
            rbm.summarize(raw_result)
