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
测试小红书"一键排版"功能的页面稳定性检测

测试目标：
1. 验证增强的 waitForPageStability 是否能正确等待三种状态
2. 观察点击"一键排版"后，DOM 变化和网络请求的完成情况

使用前提：
- 需要在 User_Data 目录中已登录小红书账号
- 需要手动进入小红书的笔记编辑页面
"""

import asyncio
import logging

from dotenv import load_dotenv

load_dotenv()

from camel.agents import ChatAgent
from camel.models import ModelFactory
from camel.toolkits import HybridBrowserToolkit
from camel.types import ModelPlatformType, ModelType

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
    ],
)

logging.getLogger('camel.toolkits.hybrid_browser_toolkit').setLevel(
    logging.DEBUG
)

# 使用保存了小红书登录状态的 User Data 目录
USER_DATA_DIR = "User_Data"

model_backend = ModelFactory.create(
    model_platform=ModelPlatformType.DEFAULT,
    model_type=ModelType.DEFAULT,
    model_config_dict={"temperature": 0.0, "top_p": 1},
)

# 配置 toolkit
web_toolkit = HybridBrowserToolkit(
    headless=False,  # 非无头模式，方便观察
    user_data_dir=USER_DATA_DIR,
    enabled_tools=[
        "browser_open",
        "browser_close",
        "browser_visit_page",
        "browser_click",
        "browser_type",
        "browser_enter",
        "browser_scroll",
        "browser_get_page_snapshot",
    ],
    browser_log_to_file=True,  # 开启日志记录
    stealth=True,
)

agent = ChatAgent(
    model=model_backend,
    tools=[*web_toolkit.get_tools()],
    max_iteration=15,
)

# 测试任务：打开小红书发布页面，输入内容，点击一键排版
TASK_PROMPT = r"""
请执行以下步骤来测试小红书的"一键排版"功能：

1. 首先打开小红书创作中心发布页面: https://creator.xiaohongshu.com/publish/publish

2. 点击写长文tab 然后点击新的创作

3. 在正文区域输入以下测试内容：
    标题：test
    正文：  
    "这是一段测试文本，用于验证一键排版功能。
   
   第一段内容在这里。
   
   第二段内容在这里。
   
   第三段内容在这里。"
   

4. 找到并点击"一键排版"按钮 

5. 完成后点击返回返回一键排版页面

6. 报告：
   - 点击按钮后是否出现 loading 状态
   - 页面最终是否成功完成排版
   - 整个过程花费的时间

注意：如果遇到登录页面，请告诉我需要先登录。
"""


async def main() -> None:
    try:
        print("=" * 60)
        print("小红书一键排版功能 - 页面稳定性测试")
        print("=" * 60)
        print(f"使用 User Data 目录: {USER_DATA_DIR}")
        print(f"启用的工具: {web_toolkit.enabled_tools}")
        print("=" * 60)

        response = await agent.astep(TASK_PROMPT)

        print("\n" + "=" * 60)
        print("Agent 响应:")
        print("=" * 60)
        print(response.msgs[0].content if response.msgs else "<no response>")

        print(response.msg.content)

        print("\nTool calls:")
        print(str(response.info['tool_calls']))

    except Exception as e:
        print(f"发生错误: {e}")
        import traceback

        traceback.print_exc()
    finally:
        print("\n关闭浏览器...")
        await web_toolkit.browser_close()
        print("浏览器已关闭。")


if __name__ == "__main__":
    asyncio.run(main())
