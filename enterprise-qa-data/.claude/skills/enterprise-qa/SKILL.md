---
name: enterprise-qa
version: 1.0.0
description: 企业智能问答助手
author:  SouvLithe
keywords:
  - /qa
  - /enterprise-qa
  - @enterprise
entrypoint: skill.py  
handler: skill.run                
---

# 企业智能问答 Skill
企业内部员工问答助手，支持数据库查询、知识库检索、SQL注入防护。

## 触发命令
- `/enterprise-qa "你的问题"`
- `/qa "问题"`
- `@enterprise 问题`

## 功能列表
1. 查询员工部门、上级、负责项目
2. 查询企业考勤、年假等规章制度
3. 自动判断员工晋升资格
4. 防护SQL注入攻击
5. 支持本地Ollama/远程API大模型

## 使用示例
/qa "张三的部门是什么？"
/enterprise-qa "王五符合晋升条件吗？"