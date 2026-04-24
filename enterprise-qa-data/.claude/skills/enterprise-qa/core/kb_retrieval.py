import os
from pathlib import Path

class KBRetrieval:
    """
    知识库检索核心类
    功能：负责企业非结构化文本数据的检索
    包含：人事制度、财务规范、晋升标准、技术规范、会议纪要等文档
    通过关键词匹配自动定位并读取对应文档，支持自动获取最新会议纪要
    """
    def __init__(self, root_path: str):
        """
        初始化知识库检索器
        :param root_path: 知识库根目录路径
        """
        # 知识库根目录，统一管理文件路径
        self.root = Path(root_path)
        # 关键词-文档映射表：根据用户问题关键词，快速匹配对应的知识库文件
        self.file_map = {
            "年假": "hr_policies.md",       # 人事制度
            "迟到": "hr_policies.md",       # 考勤规则
            "报销": "finance_rules.md",     # 财务制度
            "晋升": "promotion_rules.md",   # 晋升标准
            "技术规范": "tech_docs.md",     # 技术文档
            "会议": "meeting_notes"         # 会议纪要目录
        }
    
    def retrieve(self, question: str) -> dict:
        """
        【核心检索方法】根据用户问题，自动检索匹配的知识库文档
        1. 关键词匹配定位文档
        2. 自动读取最新会议纪要
        3. 异常处理：文件不存在/读取失败返回友好结果
        :param question: 用户输入的问题
        :return: 检索结果字典（content=文档内容, source=来源路径）
        """
        q = question.lower()
        target_file = None
        
        # 遍历关键词映射表，匹配用户问题对应的文档
        for kw, fname in self.file_map.items():
            if kw in question:
                target_file = fname
                break
        
        # 无匹配关键词，返回空结果
        if not target_file:
            return {"content": "", "source": "无匹配文档"}
        
        # 读取目标文档内容，增加异常捕获保证程序稳定
        try:
            # 特殊处理：会议纪要 -> 自动获取最新的文件
            if "meeting" in target_file:
                # 获取目录下所有md文件并排序，取最后一个（最新）
                files = sorted((self.root / "meeting_notes").glob("*.md"))
                path = files[-1] if files else None
            # 普通文档直接匹配路径
            else:
                path = self.root / target_file
                
            # 文件路径无效/不存在
            if not path or not path.exists():
                return {"content": "", "source": "文档不存在"}
                
            # 读取文档内容（UTF-8编码兼容中文）
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                
            # 返回成功结果：内容+文件来源
            return {"content": content, "source": str(path)}
        except:
            # 读取异常：权限/格式错误等
            return {"content": "", "source": "读取失败"}