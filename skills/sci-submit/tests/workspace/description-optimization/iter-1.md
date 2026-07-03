# Iteration 1 — sci-letter

**Current description:**

> Scientific manuscript cover letter writing for journal submission and revision. Use when the user asks to write, revise, or review a cover letter for a manuscript: first-submission cover letters (投稿信), revision/resubmission cover letters (修改稿投稿信), journal-specific fit arguments, or adapting an existing cover letter for a different journal. Handles TeX and Markdown output. Not for: response letters to reviewers (回复审稿人), recommendation letters, grant proposals, job applications, or general business correspondence.

## Summary

- **Pass rate:** 20/20 queries (100%)
- **Should-trigger:** 10/10 correctly triggered
- **Should-NOT-trigger:** 10/10 correctly stayed silent

## Per-query results

| Pass | Query | Expected | Triggered |
|------|-------|----------|-----------|
| ✓ | I'm submitting a revised manuscript to ACS Nano. Can you help draft a resubmi... | trigger | 3/3 |
| ✓ | 老板让我写个投稿信，第一次投不知道怎么下手，文章是讲石墨烯热导率的，想投Advanced Science。你能教教我吗？ | trigger | 3/3 |
| ✓ | 我的文章写完了，准备投Nature Materials，帮我写一封投稿信 | trigger | 3/3 |
| ✓ | 文章修改完了，准备resubmit，需要写一个revision cover letter。这次主要在格式上换了官方模板，语言也润色过了，作者加了一个人。帮... | trigger | 3/3 |
| ✓ | I need to write a cover letter for my manuscript. It's about perovskite solar... | trigger | 3/3 |
| ✓ | 投稿信需要写哪些内容？我想投国内的Science Bulletin，英文的。 | trigger | 3/3 |
| ✓ | 帮我看一下这封cover letter写得好不好，有没有需要改的地方——主要是投Nature Energy用的，我担心期刊契合度那部分没写好。 | trigger | 3/3 |
| ✓ | 之前投了Nature被desk reject了，现在要改投Science Advances，帮我把cover letter改一下，重点突出这个工作对广泛读... | trigger | 3/3 |
| ✓ | 帮我写一封推荐信，推荐我的硕士生申请清华的博士 | silent | 0/3 |
| ✓ | 我想投PNAS，听说cover letter要指定NAS member editor，这个怎么回事？帮我写的时候注意一下这个要求。 | trigger | 3/3 |
| ✓ | I need to write a detailed response to these reviewer comments. Reviewer 1 ha... | silent | 1/3 |
| ✓ | 写一封邮件给Nature Communications的编辑，问一下我的稿件NCOMMS-2026-04567审了三个月了怎么还没消息。礼貌一点。 | silent | 0/3 |
| ✓ | We got rejected from Science after review. The editor suggested we could tran... | trigger | 3/3 |
| ✓ | I need to draft a press release for our new paper that just got accepted in N... | silent | 0/3 |
| ✓ | 能帮我把这封cover letter从英文翻译成中文吗？保持原来的格式和语气。 | silent | 1/3 |
| ✓ | 我需要一封信说明我的文章从另一本期刊撤稿的原因，因为发现了一个数据处理错误。写给之前那本期刊的编辑。 | silent | 1/3 |
| ✓ | 帮我写一封求职信，我要申请深圳先进院的助理研究员岗位，我的研究方向是钙钛矿太阳能电池。 | silent | 0/3 |
| ✓ | I want to write a letter to the editor of Nature about a recent paper they pu... | silent | 0/3 |
| ✓ | 这篇文章被拒了三次了，帮我分析一下问题出在哪里。第一次投Nature Energy desk reject，第二次投Advanced Materials送... | silent | 1/3 |
| ✓ | 帮我写一份国家自然科学基金面上项目的立项依据和研究内容，题目是关于二维材料热输运的。预算80万，四年。 | silent | 0/3 |

## Failing queries

(none — all queries passed this round)
