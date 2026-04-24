import re

class IntentClassifier:
    """
    意图识别分类器核心类
    功能：通过关键词匹配，自动分析用户的提问意图
    1. 判断是否需要查询数据库 / 知识库
    2. 区分查询类型：基础查询、关联查询、时间查询、混合查询、未知查询
    为后续的查询分发提供决策依据
    """

    def classify(self, question: str) -> dict:
        """
        【核心方法】对用户问题进行意图分类
        :param question: 用户输入的原始问题字符串
        :return: 意图结果字典，包含三个字段：
                 - db_required: 是否需要查询数据库 (bool)
                 - kb_required: 是否需要查询知识库 (bool)
                 - query_type: 查询类型 (basic/join/mixed/time/unknown)
        """
        # 统一转为小写，消除大小写影响，提升匹配准确率
        q = question.lower()
        
        # 数据库业务关键词：对应结构化数据（员工、部门、项目、考勤等）
        db_keywords = ["员工", "部门", "项目", "考勤", "绩效", "邮箱", "上级", "人数", "迟到", "负责", "职级"]
        # 知识库业务关键词：对应文本制度、规则、公告等非结构化数据
        kb_keywords = ["制度", "规则", "年假", "报销", "加班", "晋升标准", "怎么算", "会议", "规范"]
        
        # 关键词匹配：判断是否需要查询对应数据源
        db_required = any(k in q for k in db_keywords)
        kb_required = any(k in q for k in kb_keywords)
        
        # 1. 混合查询：晋升判断（需要数据库数据 + 知识库规则）
        if "晋升" in q:
            return {"db_required": True, "kb_required": True, "query_type": "mixed"}
        
        # 2. 时间范围查询：考勤/迟到按月统计（仅数据库）
        if "月" in q and ("迟到" in q or "考勤" in q):
            return {"db_required": True, "kb_required": False, "query_type": "time"}
            
        # 3. 多表关联查询：部门+项目联查（仅数据库）
        if "研发部" in q and "项目" in q:
            return {"db_required": True, "kb_required": False, "query_type": "join"}
            
        # 4. 基础数据库查询（仅数据库）
        if db_required and not kb_required:
            return {"db_required": True, "kb_required": False, "query_type": "basic"}
            
        # 5. 纯知识库查询（仅制度/规则/公告）
        if kb_required and not db_required:
            return {"db_required": False, "kb_required": True, "query_type": "basic"}
            
        # 6. 无匹配关键词：未知意图
        return {"db_required": False, "kb_required": False, "query_type": "unknown"}