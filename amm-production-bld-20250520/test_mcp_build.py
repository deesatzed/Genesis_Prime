#!/usr/bin/env python
"""
Test script to verify the MCP server build works correctly.
"""

import os
import sys
import json
from pathlib import Path
from build_amm import build_amm, BuildType

def main():
    # Create a minimal test design
    print("Creating test design...")
    test_design = {
        "id": "test_mcp_build",
        "name": "Test MCP Build",
        "description": "Test design for MCP server build",
        "knowledge_sources": [],
        "adaptive_memory": {
            "enabled": True,
            "db_name_prefix": "test_amm_memory",
            "retrieval_limit": 10
        },
        "agent_prompts": {
            "system_instruction": "You are a helpful assistant.",
            "welcome_message": "Hello, how can I help you?"
        },
        "metadata": {}  # Ensure metadata is included
    }
    
    test_design_path = Path("./test_mcp_design.json")
    with open(test_design_path, "w") as f:
        json.dump(test_design, f, indent=2)
        
    print(f"Using design file: {test_design_path}")
    
    # Create a test build output directory
    output_dir = Path("./test_build")
    output_dir.mkdir(exist_ok=True)
    
    try:
        # Attempt to build with MCP server build type
        print("Building AMM with MCP server build type...")
        build_path = build_amm(
            design_json_path=str(test_design_path),
            output_root_dir=str(output_dir),
            build_type=BuildType.MCP_SERVER
        )
        
        print(f"Build succeeded! Output at: {build_path}")
        return True
    except Exception as e:
        print(f"Build failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
