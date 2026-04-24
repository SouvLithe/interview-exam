class AnswerGenerator:
    """
    回答生成器核心类
    功能：统一格式化问答结果，根据查询类型（纯数据库/纯知识库/混合查询）
    自动拼接回答内容并标注数据来源，保证输出格式统一、规范
    """

    def generate(self, intent: dict, db_result: dict, kb_result: dict) -> str:
        """
        【核心调度方法】根据用户意图，分发并生成对应格式的回答
        :param intent: 意图识别结果（标记是否需要查询数据库/知识库）
        :param db_result: 数据库查询返回结果
        :param kb_result: 知识库检索返回结果
        :return: 格式化后的最终回答文本
        """
        # 纯数据库查询场景
        if intent["db_required"] and not intent["kb_required"]:
            return self._db_answer(db_result)
        # 纯知识库查询场景
        if intent["kb_required"] and not intent["db_required"]:
            return self._kb_answer(kb_result)
        # 数据库+知识库混合查询场景
        if intent["db_required"] and intent["kb_required"]:
            return self._mixed_answer(db_result, kb_result)
        
        # 无有效查询结果时返回兜底提示
        return "未找到相关信息，请换个问题试试。"

    def _db_answer(self, res: dict) -> str:
        """
        生成【纯数据库查询】的格式化回答
        统一拼接回答文本 + 数据源标注
        :param res: 数据库查询结果字典
        :return: 带来源标注的回答
        """
        answer = res.get("text", "")
        source = res.get("source", "")
        return f"{answer}\n\n> 来源：{source}"
    
    def _kb_answer(self, res: dict) -> str:
        """
        生成【纯知识库查询】的格式化回答
        统一拼接回答文本 + 数据源标注
        :param res: 知识库检索结果字典
        :return: 带来源标注的回答
        """
        answer = res.get("text", "")
        source = res.get("source", "")
        return f"{answer}\n\n> 来源：{source}"
    
    def _mixed_answer(self, db_res: dict, kb_res: dict) -> str:
        """
        生成【混合查询】的格式化回答
        合并数据库+知识库的结果，并统一标注双来源
        :param db_res: 数据库查询结果
        :param kb_res: 知识库检索结果
        :return: 合并后带双来源标注的回答
        """
        answer = db_res.get("text", "") + "\n" + kb_res.get("text", "")
        source = f"{db_res.get('source', '')} + {kb_res.get('source', '')}"
        return f"{answer}\n\n> 来源：{source}"