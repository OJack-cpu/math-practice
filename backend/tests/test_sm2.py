"""SM-2 算法单元测试"""
import pytest
from datetime import datetime, timedelta
from sm2 import calculate_quality, sm2_update


class TestCalculateQuality:
    """测试质量评分计算"""

    def test_correct_fast_returns_5(self):
        """正确 + 快速 → 5（完美）"""
        q = calculate_quality(is_correct=True, time_spent=10, avg_time=60)
        assert q == 5

    def test_correct_normal_returns_4(self):
        """正确 + 正常速度 → 4（良好）"""
        q = calculate_quality(is_correct=True, time_spent=50, avg_time=60)
        assert q == 4

    def test_correct_slow_returns_3(self):
        """正确 + 很慢 → 3（费劲）"""
        q = calculate_quality(is_correct=True, time_spent=120, avg_time=60)
        assert q == 3

    def test_wrong_fast_returns_2(self):
        """错误 + 快速 → 2（粗心错误）"""
        q = calculate_quality(is_correct=False, time_spent=10, avg_time=60)
        assert q == 2

    def test_wrong_normal_returns_1(self):
        """错误 + 正常速度 → 1（不熟悉）"""
        q = calculate_quality(is_correct=False, time_spent=50, avg_time=60)
        assert q == 1

    def test_wrong_slow_returns_0(self):
        """错误 + 很慢 → 0（完全不会）"""
        q = calculate_quality(is_correct=False, time_spent=120, avg_time=60)
        assert q == 0

    def test_boundary_time_spent_equal_avg(self):
        """边界：耗时等于平均时间的 0.5 倍"""
        q = calculate_quality(is_correct=True, time_spent=30, avg_time=60)
        assert q == 4  # 30 is not < 30, so it's normal

    def test_boundary_time_spent_equal_avg_half(self):
        """边界：耗时刚好等于平均时间一半"""
        q = calculate_quality(is_correct=True, time_spent=29, avg_time=60)
        assert q == 5  # 29 < 30


class TestSm2Update:
    """测试 SM-2 算法核心更新逻辑"""

    def test_quality_0_resets_interval(self):
        """质量 0 → 重置间隔为 1，repetitions 归零"""
        result = sm2_update(quality=0, easiness_factor=2.5, interval=10, repetitions=5)
        assert result["interval"] == 1
        assert result["repetitions"] == 0

    def test_quality_1_resets_interval(self):
        """质量 1 → 重置"""
        result = sm2_update(quality=1, easiness_factor=2.5, interval=10, repetitions=3)
        assert result["interval"] == 1
        assert result["repetitions"] == 0

    def test_quality_2_resets_interval(self):
        """质量 2 → 重置"""
        result = sm2_update(quality=2, easiness_factor=2.5, interval=10, repetitions=3)
        assert result["interval"] == 1
        assert result["repetitions"] == 0

    def test_quality_3_first_time_interval_1(self):
        """质量 3，repetitions=0 → interval=1"""
        result = sm2_update(quality=3, easiness_factor=2.5, interval=0, repetitions=0)
        assert result["interval"] == 1
        assert result["repetitions"] == 1

    def test_quality_4_second_time_interval_6(self):
        """质量 4，repetitions=1 → interval=6"""
        result = sm2_update(quality=4, easiness_factor=2.5, interval=1, repetitions=1)
        assert result["interval"] == 6
        assert result["repetitions"] == 2

    def test_quality_5_third_time_interval_ef_product(self):
        """质量 5，第三次 → interval = 6 * EF"""
        result = sm2_update(quality=5, easiness_factor=2.5, interval=6, repetitions=2)
        expected_interval = round(6 * 2.6)
        assert result["interval"] == expected_interval
        assert result["repetitions"] == 3

    def test_easiness_factor_never_below_1_3(self):
        """EF 不能低于 1.3"""
        result = sm2_update(quality=0, easiness_factor=1.3, interval=1, repetitions=0)
        assert result["easiness_factor"] >= 1.3

    def test_easiness_factor_increases_with_good_quality(self):
        """高质量回答后 EF 增加"""
        result = sm2_update(quality=5, easiness_factor=2.5, interval=1, repetitions=0)
        assert result["easiness_factor"] > 2.5

    def test_easiness_factor_decreases_with_bad_quality(self):
        """低质量回答后 EF 降低"""
        result = sm2_update(quality=0, easiness_factor=2.5, interval=1, repetitions=0)
        assert result["easiness_factor"] < 2.5

    def test_default_parameters(self):
        """测试默认参数"""
        result = sm2_update(quality=5)
        assert result["easiness_factor"] == 2.6
        assert result["interval"] == 1
        assert result["repetitions"] == 1

    def test_next_review_date_in_future(self):
        """下次复习日期应在未来"""
        result = sm2_update(quality=5, interval=1, repetitions=1)
        next_date = datetime.fromisoformat(result["next_review_date"])
        assert next_date > datetime.utcnow() - timedelta(seconds=1)
