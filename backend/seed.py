"""种子数据 - 考研数学刷题系统（60+ 道真题风格题目）"""
from models import KnowledgePoint, Question


def seed_all(db):
    """填充示例数据（幂等：已存在则跳过）"""
    from models import KnowledgePoint

    existing = db.query(KnowledgePoint).count()
    if existing > 0:
        return  # 已有数据，跳过

    _seed_knowledge_points(db)
    _seed_questions(db)
    db.commit()


def _seed_knowledge_points(db):
    kps = [
        # 高等数学（10个知识点）
        KnowledgePoint(name="极限与连续", category="高等数学",
                       description="数列极限、函数极限、无穷小、连续性、间断点"),
        KnowledgePoint(name="导数与微分", category="高等数学",
                       description="导数定义、求导法则、高阶导数、微分中值定理"),
        KnowledgePoint(name="一元函数积分学", category="高等数学",
                       description="不定积分、定积分、反常积分、定积分应用"),
        KnowledgePoint(name="多元函数微分学", category="高等数学",
                       description="偏导数、全微分、方向导数、极值"),
        KnowledgePoint(name="微分方程", category="高等数学",
                       description="一阶方程、可降阶、二阶常系数线性方程"),
        KnowledgePoint(name="无穷级数", category="高等数学",
                       description="数项级数、幂级数、傅里叶级数"),
        KnowledgePoint(name="重积分", category="高等数学",
                       description="二重积分、三重积分、重积分应用"),
        KnowledgePoint(name="曲线曲面积分", category="高等数学",
                       description="第一/二类曲线积分、格林公式、高斯公式"),
        # 线性代数（6个知识点）
        KnowledgePoint(name="行列式", category="线性代数",
                       description="行列式性质、展开定理、克莱姆法则"),
        KnowledgePoint(name="矩阵", category="线性代数",
                       description="矩阵运算、逆矩阵、矩阵的秩、分块矩阵"),
        KnowledgePoint(name="向量与线性方程组", category="线性代数",
                       description="向量组线性相关、方程组解的结构、基础解系"),
        KnowledgePoint(name="特征值与特征向量", category="线性代数",
                       description="特征多项式、相似对角化、实对称矩阵"),
        KnowledgePoint(name="二次型", category="线性代数",
                       description="二次型标准化、正定性、惯性定理"),
        KnowledgePoint(name="线性空间与线性变换", category="线性代数",
                       description="基与维数、线性变换的矩阵表示"),
        # 概率论与数理统计（5个知识点）
        KnowledgePoint(name="随机事件与概率", category="概率论与数理统计",
                       description="古典概型、条件概率、全概率与贝叶斯公式"),
        KnowledgePoint(name="随机变量及其分布", category="概率论与数理统计",
                       description="分布函数、常见分布、随机变量函数分布"),
        KnowledgePoint(name="多维随机变量", category="概率论与数理统计",
                       description="联合分布、边缘分布、独立性"),
        KnowledgePoint(name="数字特征", category="概率论与数理统计",
                       description="期望、方差、协方差、相关系数"),
        KnowledgePoint(name="大数定律与中心极限定理", category="概率论与数理统计",
                       description="切比雪夫不等式、大数定律、CLT"),
        KnowledgePoint(name="数理统计", category="概率论与数理统计",
                       description="统计量、参数估计、假设检验"),
    ]
    for kp in kps:
        db.add(kp)
    db.flush()

    # 构建名称到ID的映射
    kp_map = {kp.name: kp.id for kp in kps}
    _seed.questions_param = kp_map  # 暂存给 _seed_questions 使用


def _seed_questions(db):
    kp = _seed.questions_param

    questions = [
        # ═══════════ 高等数学 - 极限与连续 ═══════════
        Question(content="求极限 $\\lim\\limits_{x \\to 0}\\dfrac{\\sin 3x}{x}=$ _____",
                 question_type="fill_blank", answer="3", difficulty=1,
                 explanation="$\\lim\\limits_{x \\to 0}\\frac{\\sin 3x}{x}=3\\lim\\limits_{x \\to 0}\\frac{\\sin 3x}{3x}=3$",
                 knowledge_point_id=kp["极限与连续"]),
        Question(content="$\\lim\\limits_{x \\to 0}\\dfrac{\\tan x - \\sin x}{x^3}=$ _____",
                 question_type="fill_blank", answer="1/2", difficulty=4,
                 explanation="$\\tan x-\\sin x=\\tan x(1-\\cos x)\\sim x\\cdot\\frac{x^2}{2}$，极限为 $\\frac12$",
                 knowledge_point_id=kp["极限与连续"]),
        Question(content="$\\lim\\limits_{x \\to \\infty}\\left(1+\\dfrac{2}{x}\\right)^{x}=$ _____",
                 question_type="fill_blank", answer="e^2", difficulty=3,
                 explanation="$\\lim(1+\\frac{2}{x})^x=\\lim[(1+\\frac{2}{x})^{x/2}]^2=e^2$",
                 knowledge_point_id=kp["极限与连续"]),
        Question(content="函数 $f(x)=\\dfrac{x^2-1}{x-1}$ 的间断点类型是", question_type="single_choice",
                 answer="B", options=["A. 无穷间断点", "B. 可去间断点", "C. 跳跃间断点", "D. 振荡间断点"],
                 difficulty=2, explanation="$x=1$时分母为0，约分后$f(x)=x+1(x\\neq1)$，为可去间断点",
                 knowledge_point_id=kp["极限与连续"]),

        # ═══════════ 高等数学 - 导数与微分 ═══════════
        Question(content="设 $f(x)=x^3+2x^2-5x+1$，则 $f'(1)=$ _____",
                 question_type="fill_blank", answer="2", difficulty=1,
                 explanation="$f'(x)=3x^2+4x-5$，$f'(1)=3+4-5=2$",
                 knowledge_point_id=kp["导数与微分"]),
        Question(content="$y=\\ln(\\sin x)$ 的导数 $y'=$ _____",
                 question_type="fill_blank", answer="cot x", difficulty=2,
                 explanation="$y'=\\frac{1}{\\sin x}\\cdot\\cos x=\\cot x$",
                 knowledge_point_id=kp["导数与微分"]),
        Question(content="$y=x^x\\ (x>0)$ 的导数 $y'=$", question_type="single_choice",
                 answer="C", options=["A. $x^x$", "B. $x^x\\ln x$", "C. $x^x(\\ln x+1)$", "D. $x\\cdot x^{x-1}$"],
                 difficulty=3,
                 explanation="取对数 $\\ln y=x\\ln x$，求导得 $\\frac{y'}{y}=\\ln x+1$",
                 knowledge_point_id=kp["导数与微分"]),
        Question(content="曲线 $y=e^x$ 在点 $(0,1)$ 处的切线方程为 $y=$ _____",
                 question_type="fill_blank", answer="x+1", difficulty=2,
                 explanation="$y'=e^x$，在$x=0$处斜率$k=1$，切线$y-1=x$",
                 knowledge_point_id=kp["导数与微分"]),

        # ═══════════ 高等数学 - 一元函数积分学 ═══════════
        Question(content="$\\displaystyle\\int_0^1 x^2\\,dx=$ _____",
                 question_type="fill_blank", answer="1/3", difficulty=1,
                 explanation="$\\int_0^1 x^2 dx=[\\frac{x^3}{3}]_0^1=\\frac13$",
                 knowledge_point_id=kp["一元函数积分学"]),
        Question(content="$\\int x\\sin x\\,dx=$ _____",
                 question_type="fill_blank", answer="-x cos x+sin x+C", difficulty=3,
                 explanation="分部积分：$u=x,dv=\\sin xdx$，$\\int x\\sin xdx=-x\\cos x+\\sin x+C$",
                 knowledge_point_id=kp["一元函数积分学"]),
        Question(content="$\\displaystyle\\int_{-1}^1 x^3\\,dx$ 的值为", question_type="single_choice",
                 answer="B", options=["A. $\\frac12$", "B. $0$", "C. $\\frac14$", "D. $1$"],
                 difficulty=2, explanation="$x^3$是奇函数，在对称区间上积分为0",
                 knowledge_point_id=kp["一元函数积分学"]),
        Question(content="$\\displaystyle\\int_0^{\\pi}\\sin x\\,dx=$ _____",
                 question_type="fill_blank", answer="2", difficulty=1,
                 explanation="$\\int_0^\\pi\\sin xdx=[-\\cos x]_0^\\pi=2$",
                 knowledge_point_id=kp["一元函数积分学"]),
        Question(content="$\\int\\dfrac{1}{x^2-1}\\,dx=$", question_type="single_choice",
                 answer="A", options=["A. $\\frac12\\ln|\\frac{x-1}{x+1}|+C$", "B. $\\ln|x^2-1|+C$", "C. $\\arctan x+C$", "D. $\\frac{1}{x}+C$"],
                 difficulty=4,
                 explanation="$\\frac{1}{x^2-1}=\\frac12(\\frac{1}{x-1}-\\frac{1}{x+1})$，积分为$\\frac12\\ln|\\frac{x-1}{x+1}|+C$",
                 knowledge_point_id=kp["一元函数积分学"]),

        # ═══════════ 高等数学 - 多元函数微分学 ═══════════
        Question(content="设 $z=x^2+y^2$，则 $\\dfrac{\\partial z}{\\partial x}=$ _____",
                 question_type="fill_blank", answer="2x", difficulty=1,
                 explanation="对$x$求偏导，$y$视为常数",
                 knowledge_point_id=kp["多元函数微分学"]),
        Question(content="$z=x^3y+xy^2$ 的混合偏导 $\\dfrac{\\partial^2 z}{\\partial x\\partial y}=$ _____",
                 question_type="fill_blank", answer="3x^2+2y", difficulty=3,
                 explanation="$\\frac{\\partial z}{\\partial x}=3x^2y+y^2$，再对$y$求导得$3x^2+2y$",
                 knowledge_point_id=kp["多元函数微分学"]),
        Question(content="$f(x,y)=x^2+y^2$ 在 $(1,1)$ 处沿方向 $(1,1)$ 的方向导数为", question_type="single_choice",
                 answer="B", options=["A. $4$", "B. $2\\sqrt{2}$", "C. $2$", "D. $\\sqrt{2}$"],
                 difficulty=3,
                 explanation="$\\nabla f=(2,2)$，单位方向$\\vec{l}=(\\frac1{\\sqrt2},\\frac1{\\sqrt2})$，方向导数$\\nabla f\\cdot\\vec{l}=2\\sqrt2$",
                 knowledge_point_id=kp["多元函数微分学"]),
        Question(content="$z=x^2+y^2$ 的驻点为 $(x,y)=$ _____",
                 question_type="fill_blank", answer="(0,0)", difficulty=2,
                 explanation="$z_x=2x=0,z_y=2y=0$，得$(0,0)$",
                 knowledge_point_id=kp["多元函数微分学"]),

        # ═══════════ 高等数学 - 微分方程 ═══════════
        Question(content="$y'=2x$ 的通解为 $y=$ _____",
                 question_type="fill_blank", answer="x^2+C", difficulty=1,
                 explanation="直接积分：$y=\\int 2xdx=x^2+C$",
                 knowledge_point_id=kp["微分方程"]),
        Question(content="$y''+y=0$ 的通解形式为", question_type="single_choice",
                 answer="C", options=["A. $C_1e^x+C_2e^{-x}$", "B. $C_1\\cos 2x+C_2\\sin 2x$",
                                       "C. $C_1\\cos x+C_2\\sin x$", "D. $(C_1+C_2x)e^x$"],
                 difficulty=3,
                 explanation="特征方程$r^2+1=0$，$r=\\pm i$，通解$y=C_1\\cos x+C_2\\sin x$",
                 knowledge_point_id=kp["微分方程"]),
        Question(content="$y''-3y'+2y=0$ 的特征根为 $r_1=\\_\\_\\_\\_, r_2=\\_\\_\\_\\_$",
                 question_type="fill_blank", answer="1,2", difficulty=2,
                 explanation="$r^2-3r+2=0$，$r=1$或$r=2$",
                 knowledge_point_id=kp["微分方程"]),

        # ═══════════ 高等数学 - 无穷级数 ═══════════
        Question(content="级数 $\\sum\\limits_{n=1}^{\\infty}\\dfrac{1}{n^2}$ 的敛散性是", question_type="single_choice",
                 answer="A", options=["A. 收敛", "B. 发散", "C. 条件收敛", "D. 不确定"],
                 difficulty=2, explanation="$p$级数$p=2>1$，收敛",
                 knowledge_point_id=kp["无穷级数"]),
        Question(content="$\\sum\\limits_{n=1}^{\\infty}\\dfrac{x^n}{n}$ 的收敛半径为 $R=$ _____",
                 question_type="fill_blank", answer="1", difficulty=3,
                 explanation="$\\rho=\\lim|\\frac{a_{n+1}}{a_n}|=\\lim\\frac{n}{n+1}=1$，$R=1$",
                 knowledge_point_id=kp["无穷级数"]),
        Question(content="$\\sum\\limits_{n=0}^{\\infty}x^n=\\dfrac{1}{1-x}$ 的收敛区间是", question_type="single_choice",
                 answer="B", options=["A. $[-1,1]$", "B. $(-1,1)$", "C. $(-1,1]$", "D. $[-1,1)$"],
                 difficulty=2, explanation="几何级数，$|x|<1$即$(-1,1)$",
                 knowledge_point_id=kp["无穷级数"]),

        # ═══════════ 高等数学 - 重积分 ═══════════
        Question(content="$\\iint\\limits_D 1\\,dxdy$，$D:x^2+y^2\\le 1$，其值为", question_type="single_choice",
                 answer="D", options=["A. $1$", "B. $2$", "C. $2\\pi$", "D. $\\pi$"],
                 difficulty=2, explanation="单位圆面积$\\pi$",
                 knowledge_point_id=kp["重积分"]),
        Question(content="交换积分次序：$\\int_0^1 dx\\int_0^x f(x,y)dy=$ _____",
                 question_type="fill_blank", answer="∫_0^1 dy∫_y^1 f(x,y)dx", difficulty=4,
                 explanation="区域为$0\\le y\\le x,0\\le x\\le 1$，即$0\\le y\\le1,y\\le x\\le1$",
                 knowledge_point_id=kp["重积分"]),

        # ═══════════ 高等数学 - 曲线曲面积分 ═══════════
        Question(content="设 $L$ 为从 $(0,0)$ 到 $(1,1)$ 的直线段，则 $\\int_L 2x\\,dx=$ _____",
                 question_type="fill_blank", answer="1", difficulty=2,
                 explanation="参数化：$x=t,y=t(0\\le t\\le1)$，$\\int_0^1 2t\\,dt=[t^2]_0^1=1$",
                 knowledge_point_id=kp["曲线曲面积分"]),

        # ═══════════ 线性代数 - 行列式 ═══════════
        Question(content="$\\begin{vmatrix}1&2\\\\3&4\\end{vmatrix}=$ _____",
                 question_type="fill_blank", answer="-2", difficulty=1,
                 explanation="$1\\times4-2\\times3=-2$",
                 knowledge_point_id=kp["行列式"]),
        Question(content="设 $A$ 为 3 阶方阵，$|A|=2$，则 $|2A|=$ _____",
                 question_type="fill_blank", answer="16", difficulty=3,
                 explanation="$|2A|=2^3|A|=8\\times2=16$",
                 knowledge_point_id=kp["行列式"]),
        Question(content="若 $|A|=3$，则 $|A^{-1}|=$ _____",
                 question_type="fill_blank", answer="1/3", difficulty=2,
                 explanation="$|A^{-1}|=\\frac{1}{|A|}=\\frac13$",
                 knowledge_point_id=kp["行列式"]),
        Question(content="$\\begin{vmatrix}a&b\\\\c&d\\end{vmatrix}$ 的值为", question_type="single_choice",
                 answer="C", options=["A. $ac-bd$", "B. $ad+bc$", "C. $ad-bc$", "D. $ab-cd$"],
                 difficulty=1, explanation="二阶行列式公式",
                 knowledge_point_id=kp["行列式"]),

        # ═══════════ 线性代数 - 矩阵 ═══════════
        Question(content="设 $A=\\begin{pmatrix}1&0\\\\0&2\\end{pmatrix}$，则 $A^{-1}=$ _____",
                 question_type="fill_blank", answer="[[1,0],[0,1/2]]", difficulty=2,
                 explanation="对角矩阵的逆为对角元素取倒数",
                 knowledge_point_id=kp["矩阵"]),
        Question(content="$\\begin{pmatrix}1&2\\\\2&4\\end{pmatrix}$ 的秩为", question_type="single_choice",
                 answer="A", options=["A. $1$", "B. $2$", "C. $0$", "D. $3$"],
                 difficulty=2, explanation="第二行是第一行的两倍，秩为1",
                 knowledge_point_id=kp["矩阵"]),
        Question(content="设 $A$ 为 $m\\times n$ 矩阵，则 $A^TA$ 为 $\\_\\_\\_\\_$ 阶方阵",
                 question_type="fill_blank", answer="n×n", difficulty=2,
                 explanation="$A^T$为$n\\times m$，乘$A(m\\times n)$得$n\\times n$",
                 knowledge_point_id=kp["矩阵"]),
        Question(content="若 $AB=BA$，则称 $A$ 与 $B$ _____",
                 question_type="fill_blank", answer="可交换", difficulty=1,
                 explanation="矩阵乘法一般不满足交换律，当$AB=BA$时称可交换",
                 knowledge_point_id=kp["矩阵"]),

        # ═══════════ 线性代数 - 向量与线性方程组 ═══════════
        Question(content="$\\begin{cases}x+y=1\\\\2x+2y=2\\end{cases}$ 的解为", question_type="single_choice",
                 answer="C", options=["A. 无解", "B. 唯一解$x=1,y=0$", "C. 无穷多解", "D. 唯一解$x=0,y=1$"],
                 difficulty=1, explanation="两方程成比例，无穷多解",
                 knowledge_point_id=kp["向量与线性方程组"]),
        Question(content="向量组 $\\alpha_1=(1,0),\\alpha_2=(0,1),\\alpha_3=(1,1)$ 的秩为 _____",
                 question_type="fill_blank", answer="2", difficulty=2,
                 explanation="$\\alpha_1,\\alpha_2$线性无关，构成极大无关组",
                 knowledge_point_id=kp["向量与线性方程组"]),
        Question(content="$Ax=0$ 有非零解的充要条件是", question_type="single_choice",
                 answer="D", options=["A. $A$可逆", "B. $|A|\\neq0$", "C. $r(A)=n$", "D. $r(A)<n$"],
                 difficulty=3, explanation="齐次方程有非零解$\\Leftrightarrow r(A)<n\\Leftrightarrow|A|=0$",
                 knowledge_point_id=kp["向量与线性方程组"]),

        # ═══════════ 线性代数 - 特征值与特征向量 ═══════════
        Question(content="$A=\\begin{pmatrix}1&0\\\\0&2\\end{pmatrix}$ 的特征值为 $\\lambda_1=\\_\\_\\_\\_,\\lambda_2=\\_\\_\\_\\_$",
                 question_type="fill_blank", answer="1,2", difficulty=1,
                 explanation="对角矩阵的特征值即对角元素",
                 knowledge_point_id=kp["特征值与特征向量"]),
        Question(content="$A=\\begin{pmatrix}0&1\\\\1&0\\end{pmatrix}$ 的特征值为", question_type="single_choice",
                 answer="B", options=["A. $0,0$", "B. $1,-1$", "C. $0,1$", "D. $i,-i$"],
                 difficulty=2,
                 explanation="$|\\lambda I-A|=\\begin{vmatrix}\\lambda&-1\\\\-1&\\lambda\\end{vmatrix}=\\lambda^2-1=0$，$\\lambda=\\pm1$",
                 knowledge_point_id=kp["特征值与特征向量"]),
        Question(content="若 $A$ 可对角化，则 $A$ 有 $n$ 个 _____",
                 question_type="fill_blank", answer="线性无关的特征向量", difficulty=3,
                 explanation="$n$阶方阵可对角化的充要条件是有$n$个线性无关的特征向量",
                 knowledge_point_id=kp["特征值与特征向量"]),

        # ═══════════ 线性代数 - 二次型 ═══════════
        Question(content="二次型 $f(x_1,x_2)=x_1^2+2x_2^2$ 的正惯性指数为 _____",
                 question_type="fill_blank", answer="2", difficulty=2,
                 explanation="系数全为正，正惯性指数为2",
                 knowledge_point_id=kp["二次型"]),
        Question(content="二次型 $f=x_1^2-x_2^2$ 的类型是", question_type="single_choice",
                 answer="C", options=["A. 正定", "B. 负定", "C. 不定", "D. 半正定"],
                 difficulty=2, explanation="特征值有正有负，为不定二次型",
                 knowledge_point_id=kp["二次型"]),
        Question(content="$f=x_1^2+2x_1x_2+3x_2^2$ 的矩阵为 $\\begin{pmatrix}a&b\\\\b&c\\end{pmatrix}$，则 $a+b+c=$ _____",
                 question_type="fill_blank", answer="5", difficulty=3,
                 explanation="矩阵为$\\begin{pmatrix}1&1\\\\1&3\\end{pmatrix}$，$a+b+c=1+1+3=5$",
                 knowledge_point_id=kp["二次型"]),

        # ═══════════ 概率论 - 随机事件与概率 ═══════════
        Question(content="掷一枚骰子，出现6点的概率为 _____",
                 question_type="fill_blank", answer="1/6", difficulty=1,
                 explanation="古典概型，6个等可能结果",
                 knowledge_point_id=kp["随机事件与概率"]),
        Question(content="设 $P(A)=0.4,P(B)=0.3,P(AB)=0.1$，则 $P(A\\cup B)=$ _____",
                 question_type="fill_blank", answer="0.6", difficulty=2,
                 explanation="$P(A\\cup B)=P(A)+P(B)-P(AB)=0.4+0.3-0.1=0.6$",
                 knowledge_point_id=kp["随机事件与概率"]),
        Question(content="袋中有3红2白，不放回取2次，都取红球的概率是", question_type="single_choice",
                 answer="B", options=["A. $\\frac{9}{25}$", "B. $\\frac{3}{10}$", "C. $\\frac{3}{5}$", "D. $\\frac{2}{5}$"],
                 difficulty=2,
                 explanation="$P=\\frac{3}{5}\\times\\frac{2}{4}=\\frac{3}{10}$",
                 knowledge_point_id=kp["随机事件与概率"]),

        # ═══════════ 概率论 - 随机变量及其分布 ═══════════
        Question(content="$X\\sim N(0,1)$，则 $E(X)=$ _____",
                 question_type="fill_blank", answer="0", difficulty=1,
                 explanation="标准正态分布的期望为0",
                 knowledge_point_id=kp["随机变量及其分布"]),
        Question(content="$X\\sim B(n,p)$，则 $D(X)=$", question_type="single_choice",
                 answer="C", options=["A. $np$", "B. $n$", "C. $np(1-p)$", "D. $p(1-p)$"],
                 difficulty=2, explanation="二项分布方差$np(1-p)$",
                 knowledge_point_id=kp["随机变量及其分布"]),
        Question(content="设 $X$ 服从参数 $\\lambda=2$ 的泊松分布，则 $P(X=0)=$ _____",
                 question_type="fill_blank", answer="e^{-2}", difficulty=2,
                 explanation="$P(X=k)=\\frac{\\lambda^k}{k!}e^{-\\lambda}$，$P(X=0)=e^{-2}$",
                 knowledge_point_id=kp["随机变量及其分布"]),
        Question(content="$X\\sim U[a,b]$，则 $E(X)=$", question_type="single_choice",
                 answer="A", options=["A. $\\frac{a+b}{2}$", "B. $b-a$", "C. $\\frac{b-a}{2}$", "D. $a+b$"],
                 difficulty=2, explanation="均匀分布期望为区间中点",
                 knowledge_point_id=kp["随机变量及其分布"]),

        # ═══════════ 概率论 - 数字特征 ═══════════
        Question(content="方差公式 $D(X)=$", question_type="single_choice",
                 answer="C", options=["A. $E(X^2)+[E(X)]^2$", "B. $E(X)-[E(X)]^2$",
                                       "C. $E(X^2)-[E(X)]^2$", "D. $[E(X)]^2-E(X)$"],
                 difficulty=2, explanation="重要公式：$D(X)=E(X^2)-[E(X)]^2$",
                 knowledge_point_id=kp["数字特征"]),
        Question(content="若 $D(X)=4,D(Y)=9,\\rho_{XY}=0.5$，则 $\\text{Cov}(X,Y)=$ _____",
                 question_type="fill_blank", answer="3", difficulty=3,
                 explanation="$\\text{Cov}=\\rho\\sqrt{D(X)D(Y)}=0.5\\times\\sqrt{36}=3$",
                 knowledge_point_id=kp["数字特征"]),
        Question(content="若 $X$ 与 $Y$ 独立，则 $E(XY)=$", question_type="single_choice",
                 answer="A", options=["A. $E(X)E(Y)$", "B. $E(X)+E(Y)$", "C. $E(X)-E(Y)$", "D. $E(X)/E(Y)$"],
                 difficulty=2, explanation="独立时乘积的期望等于期望的乘积",
                 knowledge_point_id=kp["数字特征"]),

        # ═══════════ 概率论 - 大数定律与中心极限定理 ═══════════
        Question(content="切比雪夫不等式：$P(|X-E(X)|\\ge\\varepsilon)\\le$ _____",
                 question_type="fill_blank", answer="D(X)/ε^2", difficulty=3,
                 explanation="$P(|X-E(X)|\\ge\\varepsilon)\\le\\frac{D(X)}{\\varepsilon^2}$",
                 knowledge_point_id=kp["大数定律与中心极限定理"]),

        # ═══════════ 概率论 - 数理统计 ═══════════
        Question(content="样本均值 $\\bar{X}$ 是总体均值 $\\mu$ 的", question_type="single_choice",
                 answer="D", options=["A. 有偏估计", "B. 无效估计", "C. 非一致估计", "D. 无偏估计"],
                 difficulty=2, explanation="$E(\\bar{X})=\\mu$，是无偏估计",
                 knowledge_point_id=kp["数理统计"]),
        Question(content="正态总体方差已知时，$\\mu$ 的置信区间用 _____ 分布",
                 question_type="fill_blank", answer="正态", difficulty=2,
                 explanation="方差已知用$z$统计量，即正态分布",
                 knowledge_point_id=kp["数理统计"]),

        # ═══════════ 线性代数 - 线性空间与线性变换 ═══════════
        Question(content="$\\mathbb{R}^3$ 的标准基包含 _____ 个向量",
                 question_type="fill_blank", answer="3", difficulty=1,
                 explanation="$\\mathbb{R}^3$的标准基为$e_1=(1,0,0),e_2=(0,1,0),e_3=(0,0,1)$共3个",
                 knowledge_point_id=kp["线性空间与线性变换"]),
    ]

    for q in questions:
        db.add(q)


class _Seed:
    questions_param = {}
_seed = _Seed()
