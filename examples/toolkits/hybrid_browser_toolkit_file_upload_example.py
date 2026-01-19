# ========= Copyright 2023-2026 @ CAMEL-AI.org. All Rights Reserved. =========
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ========= Copyright 2023-2026 @ CAMEL-AI.org. All Rights Reserved. =========
"""
Example demonstrating file upload and download capabilities
of the HybridBrowserToolkit.

This example shows how to:
1. Upload a file to a file input element on a web page
2. Download a file by clicking a download link

Prerequisites:
- Install CAMEL with browser support: pip install camel-ai[browser]
- Ensure Node.js is installed for the TypeScript backend
"""

import asyncio
import os
import tempfile

from camel.toolkits import HybridBrowserToolkit


async def demo_file_operations():
    """Demonstrate file upload and download operations."""
    
    # Create a temporary test file for upload demonstration
    with tempfile.NamedTemporaryFile(
        mode='w', suffix='.txt', delete=False
    ) as f:
        f.write("This is a test file for upload demonstration.\n")
        f.write("Created by CAMEL HybridBrowserToolkit example.\n")
        test_file_path = f.name
    
    print(f"Created test file: {test_file_path}")
    
    # Initialize the toolkit with file operation tools enabled
    toolkit = HybridBrowserToolkit(
        headless=False,  # Set to True for headless mode
        enabled_tools=[
            "browser_open",
            "browser_close",
            "browser_visit_page",
            "browser_get_page_snapshot",
            "browser_click",
            "browser_upload_file",
            "browser_download_file",
        ],
    )
    
    try:
        # Open browser
        print("\n=== Opening Browser ===")
        result = await toolkit.browser_open()
        print(f"Browser opened: {result.get('result', '')[:100]}...")
        
        # Visit a file upload test page
        # Note: You can replace this with any page that has a file input
        print("\n=== Visiting File Upload Test Page ===")
        result = await toolkit.browser_visit_page(
            "https://httpbin.org/forms/post"
        )
        print(f"Visited page: {result.get('result', '')[:100]}...")
        
        # Get page snapshot to find the file input element
        print("\n=== Getting Page Snapshot ===")
        snapshot = await toolkit.browser_get_page_snapshot()
        print("Page snapshot (first 500 chars):")
        print(snapshot[:500] if len(snapshot) > 500 else snapshot)
        print("...")
        
        # Note: The actual file upload would require finding a file input
        # element on the page. This is a demonstration of the API.
        # In a real scenario, you would:
        # 1. Parse the snapshot to find a file input element's ref ID
        # 2. Call browser_upload_file with that ref and a file path
        
        # Example of how to use file upload (commented out as it requires
        # a specific page with file input):
        # print("\n=== Uploading File ===")
        # upload_result = await toolkit.browser_upload_file(
        #     ref="e1",  # Replace with actual ref from snapshot
        #     file_path=test_file_path
        # )
        # print(f"Upload result: {upload_result}")
        
        # Visit a page with downloadable content
        print("\n=== Visiting Download Test Page ===")
        result = await toolkit.browser_visit_page(
            "https://httpbin.org/html"
        )
        print(f"Visited page: {result.get('result', '')[:100]}...")
        
        # Get snapshot to find download links
        print("\n=== Getting Page Snapshot for Downloads ===")
        snapshot = await toolkit.browser_get_page_snapshot()
        print("Page snapshot (first 500 chars):")
        print(snapshot[:500] if len(snapshot) > 500 else snapshot)
        print("...")
        
        # Example of how to use file download (commented out as it requires
        # a specific download link):
        # print("\n=== Downloading File ===")
        # download_result = await toolkit.browser_download_file(
        #     ref="e5",  # Replace with actual ref of download link
        #     save_dir="/tmp/downloads"
        # )
        # print(f"Download result: {download_result}")
        # if download_result.get("success"):
        #     print(f"File saved to: {download_result.get('file_path')}")
        #     print(f"File name: {download_result.get('file_name')}")
        #     print(f"File size: {download_result.get('file_size')} bytes")
        
        print("\n=== Demo Complete ===")
        print("To test file operations in your application:")
        print("1. Navigate to a page with file upload/download elements")
        print("2. Use browser_get_page_snapshot to find element refs")
        print("3. Use browser_upload_file(ref=..., file_path=...)")
        print("4. Use browser_download_file(ref=..., save_dir=...)")
        
    finally:
        # Clean up
        print("\n=== Closing Browser ===")
        await toolkit.browser_close()
        
        # Remove test file
        if os.path.exists(test_file_path):
            os.remove(test_file_path)
            print(f"Removed test file: {test_file_path}")


async def demo_with_agent():
    """
    Demonstrate file operations with a ChatAgent.
    
    This shows how an AI agent can use the file upload/download tools
    as part of its tool arsenal.
    """
    from camel.agents import ChatAgent
    from camel.models import ModelFactory
    from camel.types import ModelPlatformType, ModelType
    
    # Initialize the toolkit with file operation tools
    toolkit = HybridBrowserToolkit(
        headless=False,
        enabled_tools=[
            "browser_open",
            "browser_close",
            "browser_visit_page",
            "browser_get_page_snapshot",
            "browser_click",
            "browser_type",
            "browser_upload_file",
            "browser_download_file",
        ],
    )
    
    # Create a model (using GPT-4 as an example)
    model = ModelFactory.create(
        model_platform=ModelPlatformType.OPENAI,
        model_type=ModelType.GPT_4O_MINI,
    )
    
    # Create a ChatAgent with browser tools
    agent = ChatAgent(
        system_message=(
            "You are a helpful assistant that can browse the web and "
            "perform file operations. You can upload files to web pages "
            "and download files from the web."
        ),
        model=model,
        tools=toolkit.get_tools(),
    )
    
    try:
        # Example task that might use file operations
        response = agent.step(
            "Open a browser and visit httpbin.org/html. "
            "Get a snapshot of the page and describe what you see."
        )
        print("Agent response:")
        print(response.msg.content)
        
    finally:
        await toolkit.browser_close()


if __name__ == "__main__":
    print("=" * 60)
    print("HybridBrowserToolkit File Upload/Download Example")
    print("=" * 60)
    
    # Run the basic demo
    asyncio.run(demo_file_operations())
    
    # Uncomment to run the agent demo (requires API keys)
    # asyncio.run(demo_with_agent())
