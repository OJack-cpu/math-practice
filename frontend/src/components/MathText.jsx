import katex from 'katex';
import 'katex/dist/katex.min.css';

/**
 * 数学公式渲染组件
 * 自动识别文本中的 $...$（行内公式）和 $$...$$（块级公式）并渲染为数学公式
 */
export default function MathText({ text, style = {}, blockStyle = {} }) {
  if (!text) return null;

  // 先处理 $$...$$ 块级公式，再处理 $...$ 行内公式
  const parts = [];
  let remaining = text;

  // 分割：同时匹配行内和块级
  const regex = /(\$\$[\s\S]*?\$\$|\$[^$]+\$)/g;
  let lastIndex = 0;
  let match;

  while ((match = regex.exec(remaining)) !== null) {
    // 添加前面的普通文本
    if (match.index > lastIndex) {
      parts.push({
        type: 'text',
        content: remaining.slice(lastIndex, match.index),
      });
    }

    const formula = match[0];
    const isBlock = formula.startsWith('$$');
    const latex = isBlock ? formula.slice(2, -2).trim() : formula.slice(1, -1).trim();

    try {
      const html = katex.renderToString(latex, {
        displayMode: isBlock,
        throwOnError: false,
        strict: false,
      });
      parts.push({ type: 'html', content: html, isBlock });
    } catch {
      parts.push({ type: 'text', content: formula });
    }

    lastIndex = regex.lastIndex;
  }

  // 添加剩余文本
  if (lastIndex < remaining.length) {
    parts.push({ type: 'text', content: remaining.slice(lastIndex) });
  }

  if (parts.length === 0) {
    return <span style={style}>{text}</span>;
  }

  return (
    <span style={{ lineHeight: 2.2, ...style }}>
      {parts.map((part, i) =>
        part.type === 'html' ? (
          <span
            key={i}
            dangerouslySetInnerHTML={{ __html: part.content }}
            style={part.isBlock ? { display: 'block', margin: '12px 0', textAlign: 'center', ...blockStyle } : {}}
          />
        ) : (
          <span key={i}>{part.content}</span>
        )
      )}
    </span>
  );
}
