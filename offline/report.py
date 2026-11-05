"""Portable, self-contained review report; works from disk without a server."""
import html
import json
from pathlib import Path


def write_report(output):
    report = json.loads((output / "metrics.json").read_text(encoding="utf-8"))
    predictions = [json.loads(line) for line in (output / "predictions.jsonl").read_text(encoding="utf-8").splitlines()]
    table = []
    for key, value in report["results"].items():
        table.append((key, str(value["n"]), f'{value["balanced_accuracy"]:.1%}',
                      f'{value["error_recall"]:.1%}', f'{value["normal_false_alarm_rate"]:.1%}'))
    md = ["# LabPulse 无设备阶段验证结果", "", "2026-11-05｜公开数据离线研究，不代表设备或个人验证。", "",
          "固定基线：S02前300原始试次训练，中间50试次不使用，最后150试次及S03全会话独立评价。",
          "按质量剔除后计数如下；归一化仅拟合训练集。阈值0.5，未用测试集调参。", "",
          "| 测试集合 | 可判定试次 | 平衡准确率 | 机器错误检出率 | 正常误报率 |", "|---|---:|---:|---:|---:|"]
    md.extend("| " + " | ".join(row) + " |" for row in table)
    md.extend(["", "平衡准确率是两类召回率的平均；检出率低意味着漏掉了不少错误。当前不通过可靠识别器验收。",
               "跨人结果仅一个外部参与者，不作群体泛化推断；标签置换参考区间不是性能置信区间或生理特异性证明。", "",
               "## 排除和覆盖范围", ""])
    for source in report["sources"]:
        md.append(f'- {source["subject"]}：总{source["trials"]}试次，保留{source["accepted"]}；排除 {source["exclusions"]}。')
    md.extend(["", "27个EEG通道，256 Hz，排除3个EOG。数据集原有重参考和降采样无法被本流程撤销。",
               "因果滤波1–10 Hz；以FB方向反馈为锚点，取−0.2～0.8秒窗口，0.2～0.6秒分8箱取均值；",
               "原始窗口峰峰值超过200 µV则拒判。该门控读取完整0.8秒窗口，不能把0.6秒解释为当前实现的端到端时延。",
               "颜色反馈、动作及残余伪迹可能影响结果，尚不能证明ErrP来源。", "",
               "## 软件验证边界", "",
               "分类与回放已实际执行；完整数据计数、参数和哈希见 metrics.json。模型只在本地保存。",
               "LSL模拟结果单独见 lsl_simulation.json；合成正弦波不是EEG，不合并为识别成绩。",
               "实际硬件采样率、丢包、GUI Marker落盘、物理事件同步、个人ErrP识别均未验证。",
               "屏幕任务只检查了日程和语法，GUI外观、按键体验和实际显示时间待人工验证。"])
    text = "\n".join(md) + "\n"
    (output / "验证结果.md").write_text(text, encoding="utf-8")
    payload = json.dumps(predictions, ensure_ascii=False).replace("<", "\\u003c")
    body = f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>LabPulse 离线验证</title>
<style>body{{font:17px/1.7 system-ui;margin:40px auto;max-width:950px;padding:0 20px;background:#f3f5f7;color:#192a38}}pre{{white-space:pre-wrap}}section{{background:white;padding:24px;border-radius:12px;margin:20px 0}}button,select{{font:inherit;margin:6px;padding:8px}}#alert{{font-size:24px}}.warn{{color:#a12f13}}</style>
<h1>LabPulse · 公开数据回放</h1><p class="warn">本页无设备、无机械臂、无Jarvis。分类已离线计算；播放速度不是推理延迟。</p>
<section><label>测试集 <select id="set"><option value="s02_late_holdout">同人后段 S02</option><option value="s03_cross_person_holdout">跨人 S03</option></select></label>
<button id="next">下一条</button><button id="play">自动播放</button><p id="trial"></p><p id="alert"></p><p id="truth"></p></section>
<section><pre>{html.escape(text)}</pre></section>
<script>const data={payload};let index=0,timer=null;const set=document.getElementById('set');
function step(){{const rows=data.filter(x=>x.evaluation===set.value);if(index>=rows.length){{stop();return;}}const r=rows[index++];document.getElementById('trial').textContent=r.event_id+' | score='+r.score.toFixed(3);document.getElementById('alert').textContent=r.message;document.getElementById('truth').textContent='评价真值（不参与预测）：'+(r.true_label_for_evaluation?'机器错误':'正常')+'；'+index+'/'+rows.length;}}
function stop(){{clearInterval(timer);timer=null;document.getElementById('play').textContent='自动播放';}}
document.getElementById('next').onclick=step;document.getElementById('play').onclick=()=>{{if(timer){{stop();return;}}timer=setInterval(step,700);document.getElementById('play').textContent='暂停';}};set.onchange=()=>{{stop();index=0;step();}};step();</script></html>'''
    (output / "report.html").write_text(body, encoding="utf-8")


if __name__ == "__main__":
    write_report(Path("reports/offline"))
