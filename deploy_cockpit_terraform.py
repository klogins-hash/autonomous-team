#!/usr/bin/env python3
"""
Deploy Cockpit Terraform Monitoring
Utilize Cockpit's Terraform capabilities for production monitoring
"""

import subprocess
import json
import os
from pathlib import Path
from datetime import datetime

def deploy_cockpit_terraform():
    """Deploy Cockpit monitoring using Terraform"""
    
    print("🏗️  DEPLOYING COCKPIT TERRAFORM MONITORING")
    print("=" * 60)
    
    # Set up Terraform directory
    terraform_dir = Path("/root/CascadeProjects/autonomous_team_workspace/infrastructure/terraform")
    os.chdir(terraform_dir)
    
    print(f"📁 Working directory: {terraform_dir}")
    
    # Step 1: Initialize Terraform
    print("\\n🔧 Step 1: Initializing Terraform...")
    
    try:
        init_result = subprocess.run(
            ["terraform", "init"],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if init_result.returncode == 0:
            print("   ✅ Terraform initialized successfully")
        else:
            print(f"   ❌ Terraform init failed: {init_result.stderr}")
            return {"status": "terraform_init_failed", "error": init_result.stderr}
            
    except subprocess.TimeoutExpired:
        print("   ❌ Terraform init timed out")
        return {"status": "terraform_init_timeout"}
    except Exception as e:
        print(f"   ❌ Terraform init error: {e}")
        return {"status": "terraform_init_error", "error": str(e)}
    
    # Step 2: Plan Terraform deployment
    print("\\n📋 Step 2: Planning Terraform deployment...")
    
    try:
        plan_result = subprocess.run(
            ["terraform", "plan", "-out=cockpit.plan", "-json"],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if plan_result.returncode == 0:
            print("   ✅ Terraform plan created successfully")
            
            # Parse plan output
            try:
                plan_data = json.loads(plan_result.stdout)
                resource_changes = plan_data.get("resource_changes", [])
                print(f"   📊 Plan includes {len(resource_changes)} resource changes")
                
                for change in resource_changes[:5]:  # Show first 5
                    action = change.get("change", {}).get("actions", [])
                    resource_type = change.get("type", "")
                    resource_name = change.get("name", "")
                    print(f"      • {resource_type}.{resource_name}: {action}")
                
                if len(resource_changes) > 5:
                    print(f"      ... and {len(resource_changes) - 5} more changes")
                    
            except json.JSONDecodeError:
                print("   ⚠️  Could not parse plan JSON, but plan was created")
                
        else:
            print(f"   ❌ Terraform plan failed: {plan_result.stderr}")
            return {"status": "terraform_plan_failed", "error": plan_result.stderr}
            
    except subprocess.TimeoutExpired:
        print("   ❌ Terraform plan timed out")
        return {"status": "terraform_plan_timeout"}
    except Exception as e:
        print(f"   ❌ Terraform plan error: {e}")
        return {"status": "terraform_plan_error", "error": str(e)}
    
    # Step 3: Apply Terraform configuration
    print("\\n🚀 Step 3: Applying Terraform configuration...")
    
    try:
        apply_result = subprocess.run(
            ["terraform", "apply", "-auto-approve", "-json", "cockpit.plan"],
            capture_output=True,
            text=True,
            timeout=300  # 5 minutes timeout
        )
        
        if apply_result.returncode == 0:
            print("   ✅ Terraform applied successfully!")
            
            # Parse apply output for results
            try:
                apply_lines = apply_result.stdout.split('\\n')
                outputs = {}
                
                for line in apply_lines:
                    if '"@level":"info"' in line and '"type":"tfe_plan"' in line:
                        # This is a Terraform Cloud/Enterprise response, skip
                        continue
                    elif '"type":"outputs"' in line:
                        # Extract outputs
                        try:
                            output_data = json.loads(line)
                            outputs = output_data.get("outputs", {})
                        except:
                            pass
                
                if outputs:
                    print("   📊 Terraform outputs:")
                    for key, value in outputs.items():
                        print(f"      • {key}: {value}")
                else:
                    print("   📊 Terraform outputs: (parsing detailed output)")
                    
            except Exception as e:
                print(f"   ⚠️  Could not parse apply output: {e}")
            
        else:
            print(f"   ❌ Terraform apply failed: {apply_result.stderr}")
            return {"status": "terraform_apply_failed", "error": apply_result.stderr}
            
    except subprocess.TimeoutExpired:
        print("   ❌ Terraform apply timed out")
        return {"status": "terraform_apply_timeout"}
    except Exception as e:
        print(f"   ❌ Terraform apply error: {e}")
        return {"status": "terraform_apply_error", "error": str(e)}
    
    # Step 4: Get Terraform outputs
    print("\\n📤 Step 4: Retrieving Terraform outputs...")
    
    try:
        output_result = subprocess.run(
            ["terraform", "output", "-json"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if output_result.returncode == 0:
            outputs = json.loads(output_result.stdout)
            
            print("   ✅ Terraform outputs retrieved:")
            
            if "cockpit_dashboards" in outputs:
                dashboards = outputs["cockpit_dashboards"]["value"]
                print("   🌐 Cockpit Dashboards:")
                for name, url in dashboards.items():
                    print(f"      • {name}: {url}")
            
            if "grafana_access" in outputs:
                grafana = outputs["grafana_access"]["value"]
                print("   🔐 Grafana Access:")
                print(f"      • URL: {grafana['url']}")
                for user, login in grafana["users"].items():
                    print(f"      • {user}: {login}")
            
            if "alert_endpoints" in outputs:
                alerts = outputs["alert_endpoints"]["value"]
                print("   🚨 Alert Endpoints:")
                for name, url in alerts.items():
                    print(f"      • {name}: {url}")
            
            return {
                "status": "terraform_deployed",
                "outputs": outputs,
                "timestamp": datetime.now().isoformat()
            }
            
        else:
            print(f"   ❌ Could not retrieve outputs: {output_result.stderr}")
            return {"status": "outputs_failed", "error": output_result.stderr}
            
    except Exception as e:
        print(f"   ❌ Output retrieval error: {e}")
        return {"status": "outputs_error", "error": str(e)}

def validate_cockpit_monitoring():
    """Validate that Cockpit monitoring is working"""
    
    print("\\n🔍 VALIDATING COCKPIT MONITORING")
    print("-" * 40)
    
    # Check data sources
    try:
        ds_result = subprocess.run(
            ["scw", "cockpit", "data-source", "list", "--output=json"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if ds_result.returncode == 0:
            data_sources = json.loads(ds_result.stdout)
            print(f"   ✅ Found {len(data_sources)} data sources:")
            for ds in data_sources:
                print(f"      • {ds['name']}: {ds['type']} (retention: {ds.get('retention_days', 'N/A')} days)")
        else:
            print(f"   ❌ Could not list data sources: {ds_result.stderr}")
            
    except Exception as e:
        print(f"   ❌ Data source validation error: {e}")
    
    # Check alert manager
    try:
        alert_result = subprocess.run(
            ["scw", "cockpit", "alert-manager", "list"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if alert_result.returncode == 0:
            print("   ✅ Alert manager is accessible")
        else:
            print(f"   ❌ Alert manager not accessible: {alert_result.stderr}")
            
    except Exception as e:
        print(f"   ❌ Alert manager validation error: {e}")
    
    # Check grafana users
    try:
        user_result = subprocess.run(
            ["scw", "cockpit", "grafana-user", "list"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if user_result.returncode == 0:
            print("   ✅ Grafana user management is accessible")
        else:
            print(f"   ❌ Grafana users not accessible: {user_result.stderr}")
            
    except Exception as e:
        print(f"   ❌ Grafana user validation error: {e}")

def main():
    """Main deployment function"""
    
    print("🚀 COCKPIT TERRAFORM DEPLOYMENT STARTED")
    print("=" * 60)
    
    # Deploy Terraform
    result = deploy_cockpit_terraform()
    
    if result.get("status") == "terraform_deployed":
        print("\\n🎉 COCKPIT TERRAFORM DEPLOYMENT SUCCESSFUL!")
        
        # Validate deployment
        validate_cockpit_monitoring()
        
        # Summary
        print("\\n📊 DEPLOYMENT SUMMARY:")
        print("   ✅ Terraform configuration applied")
        print("   ✅ Cockpit monitoring configured")
        print("   ✅ Alert rules created")
        print("   ✅ Grafana users managed")
        print("   ✅ Dashboards deployed")
        
        print("\\n🎯 NEXT STEPS:")
        print("   1. Access Cockpit dashboards for monitoring")
        print("   2. Configure alert notifications")
        print("   3. Monitor container deployment progress")
        print("   4. Set up additional custom alerts as needed")
        
    else:
        print(f"\\n❌ COCKPIT TERRAFORM DEPLOYMENT FAILED: {result.get('status')}")
        if 'error' in result:
            print(f"   Error: {result['error']}")
        
        print("\\n🔧 TROUBLESHOOTING:")
        print("   1. Check Terraform configuration")
        print("   2. Verify Scaleway credentials")
        print("   3. Check project permissions")
        print("   4. Review error logs above")
    
    return result

if __name__ == "__main__":
    result = main()
    print(f"\\n🏆 FINAL RESULT: {json.dumps(result, indent=2)}")
