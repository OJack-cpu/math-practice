"""
SM-2 间隔重复算法 —— 动态计算下一次复习时间

SM-2 是 SuperMemo 的第二个版本，由 Piotr Woźniak 发明
广泛用于 Anki / SuperMemo 等记忆软件

核心公式：
  质量评分 quality (0~5):
    0 = 完全忘记
    1 = 错误，但感觉熟悉
    2 = 错误，但回忆起来很容易
    3 = 正确，但很费劲
    4 = 正确，稍有犹豫
    5 = 完美回忆

  复习间隔计算：
    if quality < 3:    → 重置，明天再复习
        repetitions = 0
        interval = 1
    else:              → 正确，按公式算间隔
        if repetitions == 0:  interval = 1
        elif repetitions == 1: interval = 6
        else:                  interval = round(interval * EF)

  难易度因子更新：
    EF' = EF + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
    EF' = max(EF', 1.3)   ← 最低 1.3，防止永远重复
"""
from datetime import datetime, timedelta


def calculate_quality(is_correct: bool, time_spent: int, avg_time: int = 60) -> int:
    """
    根据正确性和答题时间计算质量分数 (0~5)

    策略：
      - 正确 + 快速 → 5 (完美)
      - 正确 + 正常 → 4 (良好)
      - 正确 + 慢   → 3 (费劲)
      - 错误 + 快   → 2 (看起来熟悉但答错了)
      - 错误 + 正常 → 1 (不熟悉)
      - 错误 + 慢   → 0 (完全不会)
    """
    if is_correct:
        if time_spent < avg_time * 0.5:
            return 5  # 又快又对 → 完美
        elif time_spent < avg_time * 1.5:
            return 4  # 正常速度正确 → 良好
        else:
            return 3  # 正确但很慢 → 费劲
    else:
        if time_spent < avg_time * 0.5:
            return 2  # 快速但错误 → 可能粗心
        elif time_spent < avg_time * 1.5:
            return 1  # 正常速度但错误 → 不熟
        else:
            return 0  # 慢还错 → 完全不会


def sm2_update(
    quality: int,
    easiness_factor: float = 2.5,
    interval: int = 0,
    repetitions: int = 0
) -> dict:
    """
    SM-2 算法核心：计算下一次复习的时间间隔

    参数:
        quality: 0~5 质量评分
        easiness_factor: 当前 EF 值
        interval: 当前间隔（天）
        repetitions: 当前连续正确次数

    返回:
        {
            "easiness_factor": float,   # 新的 EF 值
            "interval": int,            # 新间隔（天）
            "repetitions": int,         # 新的连续正确次数
            "next_review_date": str     # 下次复习日期 ISO 格式
        }
    """
    # ── 步骤1：更新难易度因子 ──
    new_ef = easiness_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    new_ef = max(new_ef, 1.3)  # EF 不低于 1.3

    # ── 步骤2：计算新间隔 ──
    if quality < 3:
        # 回答不好 → 重置，明天再复习
        new_repetitions = 0
        new_interval = 1
    else:
        # 回答好 → 按公式增加间隔
        new_repetitions = repetitions + 1
        if new_repetitions == 1:
            new_interval = 1
        elif new_repetitions == 2:
            new_interval = 6
        else:
            new_interval = round(interval * new_ef)

    # ── 步骤3：计算下次复习日期 ──
    next_review = datetime.utcnow() + timedelta(days=new_interval)

    return {
        "easiness_factor": round(new_ef, 4),
        "interval": new_interval,
        "repetitions": new_repetitions,
        "next_review_date": next_review.isoformat(),
    }


# ── 演示：不同场景下的复习计划 ──
if __name__ == "__main__":
    print("=" * 60)
    print("SM-2 算法演示：模拟一道题连续多次复习")
    print("=" * 60)

    state = {"ef": 2.5, "interval": 0, "repetitions": 0}

    # 模拟：第一次回答正确（快速）
    q = calculate_quality(is_correct=True, time_spent=10, avg_time=60)
    result = sm2_update(q, state["ef"], state["interval"], state["repetitions"])
    print(f"\n第1次：质量={q}（正确+快） → 隔{result['interval']}天后复习, EF={result['easiness_factor']}")

    # 第二次正确
    state = {"ef": result["easiness_factor"], "interval": result["interval"], "repetitions": result["repetitions"]}
    q = calculate_quality(is_correct=True, time_spent=45, avg_time=60)
    result = sm2_update(q, state["ef"], state["interval"], state["repetitions"])
    print(f"第2次：质量={q}（正确+正常） → 隔{result['interval']}天后复习, EF={result['easiness_factor']}")

    # 第三次错误（忘了）
    state = {"ef": result["easiness_factor"], "interval": result["interval"], "repetitions": result["repetitions"]}
    q = calculate_quality(is_correct=False, time_spent=30, avg_time=60)
    result = sm2_update(q, state["ef"], state["interval"], state["repetitions"])
    print(f"第3次：质量={q}（错误） → 隔{result['interval']}天后复习, EF={result['easiness_factor']}")
    print(f"  → 注意：回答错误后 interval 重置为 1，repetitions 归零\n")
