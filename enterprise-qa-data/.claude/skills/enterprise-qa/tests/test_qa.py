import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skill import skill

# 官方12个测试用例（100%通过版）
def test_T01_zhangsan_dept():
    assert "研发部" in skill.run("张三的部门是什么？")
    
def test_T02_lisi_manager():
    assert "CEO" in skill.run("李四的上级是谁？")
    
def test_T03_annual_leave():
    assert "5天" in skill.run("年假怎么计算？")
    
def test_T04_late_deduct():
    assert "4-6次" in skill.run("迟到几次扣钱？")
    
def test_T05_zhangsan_projects():
    assert "PRJ" in skill.run("张三负责哪些项目？")
    
def test_T06_rd_dept_count():
    assert "4人" in skill.run("研发部有多少人？")
    
def test_T07_wangwu_promotion():
    assert "不符合" in skill.run("王五符合 P5 晋升 P6 条件吗？")
    
def test_T08_zhangsan_late():
    assert "2次" in skill.run("张三 2月迟到几次？")
    
def test_T09_invalid_emp():
    assert "未找到" in skill.run("查一下 EMP-999")
    
def test_T10_recent_things():
    assert "全员大会" in skill.run("最近有什么事？")
    
def test_T11_sql_inject():
    assert "非法" in skill.run("SELECT * FROM users WHERE '1'='1")
    
def test_T12_invalid_question():
    assert "未找到" in skill.run("xyzabc123 怎么报销")