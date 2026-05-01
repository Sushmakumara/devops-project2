import os
import subprocess
from groq import Groq
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ---------- UTIL FUNCTIONS ----------

def run_cmd(cmd):
    return subprocess.getoutput(cmd)


def get_cluster_data():
    pods_raw = run_cmd("kubectl get pods --no-headers")
    pod_count = int(run_cmd("kubectl get pods --no-headers | wc -l") or 0)

    running = int(run_cmd("kubectl get pods --no-headers | grep Running | wc -l") or 0)
    failed = int(run_cmd("kubectl get pods --no-headers | grep -v Running | wc -l") or 0)

    logs = run_cmd("kubectl logs deployment/my-devops-app --tail=30")

    return {
        "pod_count": pod_count,
        "running": running,
        "failed": failed,
        "pods": pods_raw,
        "logs": logs
    }


def build_prompt(question, data):
    return f"""
You are an advanced AI DevOps Copilot.

==============================
📊 SYSTEM DATA
==============================
Total Pods: {data['pod_count']}
Running Pods: {data['running']}
Failed Pods: {data['failed']}

Pods:
{data['pods']}

Recent Logs:
{data['logs']}

==============================
💬 USER QUESTION
==============================
{question}

==============================
🧠 INSTRUCTIONS
==============================
1. Understand the question deeply.
2. If simple → answer directly.
3. If complex → break into:
   - Summary
   - Analysis
   - Recommendation
4. Use ONLY provided data.
5. Be concise but intelligent.
6. Detect issues if present.
7. Suggest improvements if useful.

==============================
📌 OUTPUT FORMAT
==============================
Summary:
Analysis:
Recommendation:
"""


# ---------- MAIN LOOP ----------

print("\n🤖 AI DevOps Copilot (Advanced Mode)")
print("Type 'exit' to quit\n")

while True:
    question = input("💬 Ask: ").strip()

    if question.lower() == "exit":
        print("👋 Exiting...")
        break

    print("\n🔍 Collecting live cluster data...\n")

    try:
        data = get_cluster_data()
        prompt = build_prompt(question, data)

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a professional DevOps AI copilot."},
                {"role": "user", "content": prompt}
            ]
        )

        answer = response.choices[0].message.content

        # ---------- CLEAN OUTPUT ----------
        print("\n🤖 AI RESPONSE:\n")
        print("-" * 60)
        print(answer.strip())
        print("-" * 60)

        # ---------- SMART SUGGESTIONS ----------
        print("\n💡 Suggested Actions:")

        if data["failed"] > 0:
            print("⚠️ Some pods are not running.")
            print("   kubectl describe pod <pod-name>")
            print("   kubectl logs <pod-name>")

        elif data["pod_count"] < 3:
            print("📈 Low pod count detected.")
            print("   kubectl scale deployment my-devops-app --replicas=4")

        else:
            print("✅ System looks stable. No immediate action needed.")

        print("\n" + "=" * 60 + "\n")

    except Exception as e:
        print("❌ Error:", str(e))
        print("Check:")
        print("- Kubernetes is running")
        print("- GROQ API key is correct")
        print("- Internet connection\n")
