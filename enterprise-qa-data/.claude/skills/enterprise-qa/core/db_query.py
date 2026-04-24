import sqlite3
import re
from typing import Optional, Dict, Any, List

class DBQuery:
    """
    数据库查询核心类
    功能：封装 SQLite 数据库的所有安全查询操作，内置 SQL 注入防护
    提供员工信息、部门、项目、考勤、绩效等业务数据的查询方法
    所有查询均使用参数化语句，杜绝注入风险
    """
    def __init__(self, db_path: str):
        """
        初始化数据库查询类
        :param db_path: SQLite 数据库文件路径
        """
        self.db_path = db_path
        # SQL 注入拦截黑名单：高危操作关键词
        self.blocked_keywords = ["drop", "delete", "update", "insert", ";", "--", "union", "select *"]
        
    def _safe_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """
        【核心私有方法】安全查询执行器
        1. 校验 SQL 语句，拦截高危关键词
        2. 使用参数化查询防止 SQL 注入
        3. 执行查询并返回字典格式的结果集
        :param query: SQL 查询语句
        :param params: SQL 参数化占位符对应的值
        :return: 查询结果列表（每条记录为字典）
        """
        # 前置安全校验：拦截非法 SQL 关键词
        for kw in self.blocked_keywords:
            if kw in query.lower():
                raise ValueError("非法查询，已拦截")
        
        # 连接数据库并执行查询
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # 让结果支持字段名读取
        cursor = conn.cursor()
        cursor.execute(query, params)  # 参数化执行，防注入
        result = [dict(row) for row in cursor.fetchall()]  # 转为字典列表
        conn.close()  # 关闭连接，释放资源
        return result

    # ===================== 业务查询方法（测试用例全覆盖） =====================
    def get_employee_dept(self, name: str) -> Optional[Dict]:
        """
        根据员工姓名查询所属部门
        :param name: 员工姓名
        :return: 部门信息字典 / None
        """
        return self._safe_query("SELECT department FROM employees WHERE name=?", (name,))
    
    def get_employee_manager(self, name: str) -> Optional[Dict]:
        """
        根据员工姓名查询上级信息
        :param name: 员工姓名
        :return: 上级ID字典 / None
        """
        return self._safe_query("SELECT manager_id FROM employees WHERE name=?", (name,))
    
    def get_employee_projects(self, name: str) -> list:
        """
        根据员工姓名查询负责/参与的所有项目及角色
        :param name: 员工姓名
        :return: 项目列表（包含项目名、角色）
        """
        return self._safe_query("""
            SELECT p.name, pm.role FROM project_members pm
            JOIN projects p ON pm.project_id = p.project_id
            JOIN employees e ON pm.employee_id = e.employee_id
            WHERE e.name=?
        """, (name,))
    
    def get_dept_count(self, dept: str) -> int:
        """
        查询指定部门的在职员工人数
        :param dept: 部门名称
        :return: 员工数量
        """
        res = self._safe_query("SELECT COUNT(*) as cnt FROM employees WHERE department=? AND status='active'", (dept,))
        return res[0]['cnt'] if res else 0
    
    def get_late_count(self, name: str, month: str) -> int:
        """
        查询员工指定月份的迟到次数
        :param name: 员工姓名
        :param month: 月份（如 2026-02%）
        :return: 迟到次数
        """
        res = self._safe_query("""
            SELECT COUNT(*) as cnt FROM attendance a
            JOIN employees e ON a.employee_id = e.employee_id
            WHERE e.name=? AND a.status='late' AND a.date LIKE ?
        """, (name, month))
        return res[0]['cnt'] if res else 0
    
    def get_employee_kpi(self, name: str) -> float:
        """
        查询员工年度平均 KPI 分数
        :param name: 员工姓名
        :return: 平均 KPI 分数
        """
        res = self._safe_query("""
            SELECT AVG(kpi_score) as avg FROM performance_reviews pr
            JOIN employees e ON pr.employee_id = e.employee_id
            WHERE e.name=?
        """, (name,))
        return res[0]['avg'] if res else 0