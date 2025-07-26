# test_qloo_comprehensive.py
import asyncio
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.qloo_tag_discovery import QlooTagDiscovery
from services.qloo_entity_discovery import QlooEntityDiscovery  
from services.qloo_parameter_testing import QlooParameterTesting

async def run_comprehensive_qloo_tests():
    """Run all Qloo API tests systematically"""
    
    print("🧪 Starting Comprehensive Qloo API Testing")
    print("=" * 60)
    
    # Test 1: Tag URN Discovery
    print("\n1️⃣ TESTING TAG URN DISCOVERY")
    print("-" * 30)
    
    tag_discovery = QlooTagDiscovery()
    tag_results = await tag_discovery.discover_tag_categories()
    preference_mappings = await tag_discovery.test_preference_to_tag_mapping()
    
    print(f"\n📊 Tag Discovery Results:")
    print(f"   Categories found: {len(tag_results)}")
    print(f"   Preference mappings: {len(preference_mappings)}")
    
    # Test 2: Entity ID Discovery
    print("\n2️⃣ TESTING ENTITY ID DISCOVERY")
    print("-" * 30)
    
    entity_discovery = QlooEntityDiscovery()
    entity_results = await entity_discovery.test_entity_discovery_workflow()
    
    successful_workflows = sum(1 for r in entity_results.values() if r.get("workflow_success"))
    print(f"\n📊 Entity Discovery Results:")
    print(f"   Successful workflows: {successful_workflows}/{len(entity_results)}")
    
    # Test 3: Parameter Combinations
    print("\n3️⃣ TESTING PARAMETER COMBINATIONS")
    print("-" * 30)
    
    param_testing = QlooParameterTesting()
    param_results = await param_testing.test_parameter_combinations()
    
    successful_combinations = sum(1 for r in param_results.values() if r.get("success"))
    print(f"\n📊 Parameter Testing Results:")
    print(f"   Successful combinations: {successful_combinations}/{len(param_results)}")
    
    # Summary
