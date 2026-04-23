## 使用

1.配置环境

```bash
cd 到requirements.txt所用目录
# 安装依赖
pip install -r requirements.txt
```

2.配置 LLM 模式（二选一）

```yaml
llm:
  type: ollama
  model: deepseek-r1:8b  # 本地部署的模型名
  base_url: http://localhost:11434  # Ollama 默认地址
  api_key: "" # 此时为空

llm:
  type: remote
  model: gpt-3.5-turbo  # 或 Claude 模型
  api_key: your-api-key
  base_url: https://api.openai.com/v1  # 对应平台地址
```

3.运行测试（验证功能）

```bash
# 执行全部 12 个测试用例
python -m pytest .claude/skills/enterprise-qa/tests/test_qa.py -v

# 测试通过标准：12 个用例全部 PASSED
```

3.1 Claude测试

```claude
请记住：
当我输入 /qa、/enterprise-qa、@enterprise 开头的指令时，
读取 {SKILL.md的绝对路径}，
执行其中配置的 entrypoint（skill.py）的 handler（skill.run），提取引号内的问题并返回结果；
执行时默认选「Yes, and don’t ask again for: python *」，直接输出结果，无额外解释。
```

SKILL.md的绝对路径最好在目录中copy出来。

```claude
/qa "张三的部门是什么？"
	
	张三的部门是 研发部。
> 来源：employees 表

/enterprise-qa "年假怎么计算？"

入职满1年享5天，每增1年+1天，上限15天
> 来源：hr_policies.md

@enterprise "王五符合晋升条件吗？"

王五目前不符合 P5→P6 晋升条件。
分析：入职满2年 ✓，KPI平均80<85 ✗，项目1个<3个 ✗
> 来源：promotion_rules.md + 数据库表
```

4.触发 Skill（Claude 桌面端）

```claude
/qa "张三的部门是什么？"
/enterprise-qa "年假怎么计算？"
@enterprise "王五符合晋升条件吗？"
```

## 核心目录

```
enterprise-qa-data/
├── .claude/skills/enterprise-qa/  # Skill 核心代码
│   ├── core/          # 模块化工具（意图识别/数据库/知识库等）
│   ├── tests/         # 测试用例（12个核心场景）
│   ├── config.yaml    # 配置文件（LLM/路径等）
│   ├── skill.py       # 核心入口
│   └── SKILL.md       # Claude 官方技能说明
├── knowledge/         # 知识库（人事制度/晋升规则等）
├── enterprise.db      # 核心数据库（员工/考勤/项目等）
└── requirements.txt   # 依赖清单
```

## 支持功能

员工信息查询：部门、上级、负责项目、考勤记录、KPI

企业制度检索：年假规则、迟到扣款、报销规范、晋升标准

安全防护：SQL 注入拦截、高危操作屏蔽

智能回答：自动格式化结果 + 数据源标注，提升可读性

## 覆盖场景

| 测试类型   | 覆盖场景                                     |
| ---------- | -------------------------------------------- |
| 数据库查询 | 员工部门 / 上级 / 项目 / 迟到次数 / 部门人数 |
| 知识库检索 | 年假规则 / 迟到扣款 / 企业最新动态           |
| 混合查询   | 员工晋升资格判断                             |
| 安全防护   | SQL 注入拦截                                 |
| 异常处理   | 无效查询 / 文件不存在兜底                    |