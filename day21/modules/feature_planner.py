"""功能优化规划模块。

Day 21 要求“增加功能、用户体验优化”。
这个模块根据项目类型生成后续优化清单。
"""

from __future__ import annotations


class FeaturePlanner:
    """功能优化规划器。"""

    def suggest_features(self, project_name: str) -> dict:
        """根据项目名称给出功能优化建议。"""
        lower = project_name.lower()

        if "day19" in lower:
            features = [
                "增加 sources 命令：展示每次回答引用了哪些文档",
                "增加 rebuild 命令：删除旧向量库并重新索引 documents",
                "增加 eval 命令：运行固定问题集评估 RAG 效果",
                "增加 history 命令：查看最近提问记录",
                "优化 Prompt：要求模型只根据上下文回答，并在资料不足时说明",
            ]
        elif "day20" in lower:
            features = [
                "增加 help 命令：展示所有命令和示例",
                "增加 apply-dry-run：展示草案落地后的文件差异预览",
                "增加 validate 命令：给出运行测试或语法检查建议",
                "增加 focus 命令：设置默认关注文件",
                "优化 change set：补充风险等级和验证命令",
            ]
        else:
            features = [
                "补充 help 命令",
                "补充 README 运行示例",
                "补充测试建议",
                "优化错误提示",
                "保存运行结果到 output/",
            ]

        return {
            "project": project_name,
            "features": [
                {"id": index + 1, "title": feature, "priority": "high" if index < 2 else "medium"}
                for index, feature in enumerate(features)
            ],
        }
