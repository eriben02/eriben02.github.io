import os
import subprocess
import sys

SCRIPTS = os.path.dirname(os.path.abspath(__file__))

def run(script):
    subprocess.run([sys.executable, os.path.join(SCRIPTS, script)], check=True, cwd=SCRIPTS)

run("build_part1.py")
run("build_part2.py")
run("build_zendesk_ai_page.py")
run("build_gumroad_whop_lemonsqueezy_page.py")
run("build_queued_batch1.py")
run("build_workspace_m365_hipaa_page.py")
run("build_jotform_wix_guide.py")
run("build_hubspot_onboarding_calculator.py")
run("build_intercom_fin_calculator.py")
run("build_zoominfo_renewal_page.py")
run("build_chargeback_calculator.py")
run("update_meta_files.py")
print("Full SaaSBill build + dynamic freshness metadata completed.")
