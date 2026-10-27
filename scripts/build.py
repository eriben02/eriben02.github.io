import subprocess
import sys

subprocess.run([sys.executable, "/workspace/saastruth/scripts/build_part1.py"], check=True)
subprocess.run([sys.executable, "/workspace/saastruth/scripts/build_part2.py"], check=True)
subprocess.run([sys.executable, "/workspace/saastruth/scripts/build_zendesk_ai_page.py"], check=True, cwd="/workspace/saastruth/scripts")
subprocess.run([sys.executable, "/workspace/saastruth/scripts/build_gumroad_whop_lemonsqueezy_page.py"], check=True, cwd="/workspace/saastruth/scripts")
subprocess.run([sys.executable, "/workspace/saastruth/scripts/build_queued_batch1.py"], check=True, cwd="/workspace/saastruth/scripts")
subprocess.run([sys.executable, "/workspace/saastruth/scripts/build_workspace_m365_hipaa_page.py"], check=True, cwd="/workspace/saastruth/scripts")
subprocess.run([sys.executable, "/workspace/saastruth/scripts/build_jotform_wix_guide.py"], check=True, cwd="/workspace/saastruth/scripts")
subprocess.run([sys.executable, "/workspace/saastruth/scripts/update_meta_files.py"], check=True)
print("Full SaaSBill build + dynamic freshness metadata completed.")
