#!/usr/bin/env python3
"""
GitBook Markdown → Astro MDX 변환 스크립트
이미지(figure) 복원 포함
"""
import re
import os

# ---- 파일 매핑 ----
FILE_MAP = {
    # research
    "research/ai-agent-agentic-ai.md": "ai-agent-agentic-ai.mdx",
    "research/chill-function-calling.md": "chill-function-calling.mdx",
    "research/chroma-chunking.md": "chroma-chunking.mdx",
    "research/chunk.md": "chunk.mdx",
    "research/chunking.md": "chunking.mdx",
    "research/compounded-ai-system-the-shift-from-models-to-compound-ai-systems.md": "compounded-ai-system-the-shift-from-models-to-compound-ai-systems.mdx",
    "research/editorial-thinking.md": "editorial-thinking.mdx",
    "research/embedding.md": "embedding.mdx",
    "research/essence-of-rag.md": "essence-of-rag.mdx",
    "research/generations-never-easy.md": "generations-never-easy.mdx",
    "research/golden-gate-claude-review.md": "golden-gate-claude-review.mdx",
    "research/how-to-reduce-hallucinations.md": "how-to-reduce-hallucinations.mdx",
    "research/linguistic-prompts.md": "linguistic-prompts.mdx",
    "research/llm-grounding.md": "llm-grounding.mdx",
    "research/llm-quantization.md": "llm-quantization.mdx",
    "research/llm.md": "llm.mdx",
    "research/max-positional-embedding.md": "max-positional-embedding.mdx",
    "research/model-context-protocol.md": "model-context-protocol.mdx",
    "research/rag-1.md": "rag-1.mdx",
    "research/rag.md": "rag.mdx",
    "research/uv.md": "uv.mdx",
    # conference
    "conference/2024.md": "2024-retrospective.mdx",
    "conference/3.md": "pangyo-seminar-march-2025.mdx",
    "conference/7-kako-tech-meet-up.md": "7-kako-tech-meet-up.mdx",
    "conference/feat.-1.md": "korean-llm-open-access-1.mdx",
    "conference/feat.-2.md": "korean-llm-open-access-2.mdx",
    "conference/gdgxgdsc-devfest-happy-career.md": "gdgxgdsc-devfest-happy-career.mdx",
    "conference/langchainopentutorial.md": "langchainopentutorial.mdx",
    "conference/moducon-2023.md": "moducon-2023.mdx",
    "conference/session.md": "personalization-system-session-review.mdx",
    "conference/talk-prompt-and-language-the-science-of-prompts.md": "talk-prompt-and-language-the-science-of-prompts.mdx",
    "conference/undefined.md": "first-job-change-review.mdx",
}

SOURCE_BASE = "/Users/choijaehun/Desktop/ash-world/_reference/ash-space"
TARGET_BASE = "/Users/choijaehun/Desktop/ash-world/src/content/posts"


def parse_date(desc: str) -> str:
    """날짜 문자열을 YYYY-MM-DD 형식으로 변환"""
    desc = desc.strip()
    # 2025.01.12. 형식
    m = re.match(r'^(\d{4})\.(\d{1,2})\.(\d{1,2})\.?$', desc)
    if m:
        return f"{m.group(1)}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"
    # 2024년 11월 3일 형식
    m = re.match(r'^(\d{4})년\s*(\d{1,2})월\s*(\d{1,2})일$', desc)
    if m:
        return f"{m.group(1)}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"
    # 이미 YYYY-MM-DD
    m = re.match(r'^(\d{4}-\d{2}-\d{2})$', desc)
    if m:
        return m.group(1)
    # 2025.03.09 (마침표 없음)
    m = re.match(r'^(\d{4})\.(\d{1,2})\.(\d{1,2})$', desc)
    if m:
        return f"{m.group(1)}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"
    return desc


def extract_caption_text(figcaption_content: str) -> str:
    """figcaption 내부 HTML에서 순수 텍스트 추출"""
    # <p>...</p> 내부 텍스트
    m = re.search(r'<p>(.*?)</p>', figcaption_content, re.DOTALL)
    if m:
        text = m.group(1)
    else:
        text = figcaption_content

    # HTML 태그 제거 (<a href="...">, </a>, <strong>, <em>, <br> 등)
    text = re.sub(r'<[^>]+>', '', text)
    # &#x20; → 공백
    text = text.replace('&#x20;', ' ')
    # &#x26; → &
    text = text.replace('&#x26;', '&')
    # 기타 HTML entity
    text = re.sub(r'&#x[0-9a-fA-F]+;', '', text)
    # 앞뒤 공백 정리
    text = text.strip()
    return text


def convert_figure(match) -> str:
    """<figure>...</figure> 블록을 마크다운 이미지로 변환"""
    block = match.group(0)

    # src 추출
    src_m = re.search(r'<img\s[^>]*src="([^"]+)"', block)
    if not src_m:
        return ''
    src = src_m.group(1)

    # gitbook assets 경로 변환
    if '../.gitbook/assets/' in src:
        filename = src.replace('../.gitbook/assets/', '')
        img_path = f"/assets/{filename}"
    else:
        # 외부 URL은 그대로
        img_path = src

    # figcaption 추출
    cap_m = re.search(r'<figcaption>(.*?)</figcaption>', block, re.DOTALL)
    if cap_m:
        caption = extract_caption_text(cap_m.group(1))
    else:
        # alt 사용
        alt_m = re.search(r'<img\s[^>]*alt="([^"]*)"', block)
        caption = alt_m.group(1) if alt_m else ''

    return f"![{caption}]({img_path})"


def convert_hint(match) -> str:
    """{% hint style="..." %}...{% endhint %} → > 인용 블록"""
    content = match.group(1).strip()
    # 각 줄에 > 붙이기
    lines = content.split('\n')
    result = '\n'.join(f"> {line}" if line.strip() else '>' for line in lines)
    return result


def convert_mark(match) -> str:
    """<mark style="...">텍스트</mark> → **텍스트**"""
    text = match.group(1)
    # 내부 HTML 태그 제거
    text = re.sub(r'<[^>]+>', '', text)
    return f"**{text}**"


def escape_jsx_braces(text: str) -> str:
    """중괄호 {expr} 를 백틱으로 감싸되, 마크다운 코드블록 내부는 건드리지 않음"""
    # 코드 블록(```) 보호
    code_blocks = []
    def save_code(m):
        code_blocks.append(m.group(0))
        return f"\x00CODEBLOCK{len(code_blocks)-1}\x00"

    text = re.sub(r'```[\s\S]*?```', save_code, text)
    # 인라인 코드 보호
    inline_codes = []
    def save_inline(m):
        inline_codes.append(m.group(0))
        return f"\x00INLINE{len(inline_codes)-1}\x00"
    text = re.sub(r'`[^`]+`', save_inline, text)

    # frontmatter 바깥에서 { } 처리
    # JSX에서 문제가 될 수 있는 { } 패턴 (수식, 코드 예제 등)
    # 단독으로 서있는 {expr} 형태만 처리
    def escape_braces(m):
        inner = m.group(1)
        # 이미 백틱으로 감싸진 건 건드리지 않음
        return f"`{{{inner}}}`"

    # { ... } 패턴 - JSX 표현식처럼 보이는 것들
    # 단, 마크다운 링크 [text](...) 안의 {} 제외
    text = re.sub(r'(?<!`)\{([^{}\n]+)\}(?!`)', escape_braces, text)

    # 복원
    for i, block in enumerate(inline_codes):
        text = text.replace(f"\x00INLINE{i}\x00", block)
    for i, block in enumerate(code_blocks):
        text = text.replace(f"\x00CODEBLOCK{i}\x00", block)

    return text


def convert_math_block(content: str) -> str:
    """$$...$$ 수식 처리:
    - 독립 블록 (줄 전체가 $$로 시작/끝): 코드 블록
    - 인라인 (같은 줄 또는 짧은 $$...$$): 백틱 인라인
    """
    def replace_math(m):
        formula = m.group(1)
        # 멀티라인이면 블록 수식
        if '\n' in formula:
            return f"```\n{formula.strip()}\n```"
        else:
            # 인라인 수식
            return f"`{formula.strip()}`"
    return re.sub(r'\$\$(.*?)\$\$', replace_math, content, flags=re.DOTALL)


def convert_math_inline(content: str) -> str:
    """$수식$ 인라인 수식 → 백틱"""
    def replace_inline(m):
        formula = m.group(1)
        return f"`{formula}`"
    # 인라인 수식 (< 또는 > 포함하거나, 일반적인 수식)
    return re.sub(r'\$([^$\n]+)\$', replace_inline, content)


def convert_content(raw: str, src_path: str) -> str:
    """GitBook 마크다운을 Astro MDX 본문으로 변환"""

    # 1. <figure>...</figure> → ![caption](/assets/file.png)
    content = re.sub(r'<figure>.*?</figure>', convert_figure, raw, flags=re.DOTALL)

    # 2. {% hint style="..." %}...{% endhint %} → > 인용 블록
    content = re.sub(
        r'\{%\s*hint\s+style="[^"]*"\s*%\}(.*?)\{%\s*endhint\s*%\}',
        convert_hint,
        content,
        flags=re.DOTALL
    )

    # 2b. {% embed url="..." %}...{% endembed %} → URL 링크로 변환
    def convert_embed(m):
        url_m = re.search(r'url="([^"]+)"', m.group(0))
        if url_m:
            url = url_m.group(1)
            return f"[{url}]({url})"
        return ''
    content = re.sub(
        r'\{%\s*embed\s+url="[^"]*"\s*%\}.*?\{%\s*endembed\s*%\}',
        convert_embed,
        content,
        flags=re.DOTALL
    )
    # 혹시 endembed 없이 단독으로 남은 것
    content = re.sub(r'\{%\s*embed\s+url="([^"]*)"\s*%\}', lambda m: f"[{m.group(1)}]({m.group(1)})", content)
    content = re.sub(r'\{%\s*endembed\s*%\}', '', content)

    # 3. <mark style="...">텍스트</mark> → **텍스트**
    content = re.sub(r'<mark\s+style="[^"]*">(.*?)</mark>', convert_mark, content, flags=re.DOTALL)

    # 4. &#x20; → 공백
    content = content.replace('&#x20;', ' ')
    content = content.replace('&#x26;', '&')
    # 기타 HTML entity
    content = re.sub(r'&#x[0-9a-fA-F]+;', '', content)

    # 5. 줄 끝 \ 제거 (뒤에 공백+줄바꿈 또는 줄바꿈)
    content = re.sub(r'\\\s*\n', '\n', content)
    content = re.sub(r'\\\s*$', '', content, flags=re.MULTILINE)

    # 6. $$ 블록 수식 → 코드 블록
    content = convert_math_block(content)

    # 7. $ 인라인 수식 → 백틱 (코드블록 내부 제외)
    # 코드 블록 보호
    code_blocks = []
    def save_code(m):
        code_blocks.append(m.group(0))
        return f"\x00CODEBLOCK{len(code_blocks)-1}\x00"
    content = re.sub(r'```[\s\S]*?```', save_code, content)

    content = convert_math_inline(content)

    # 복원
    for i, block in enumerate(code_blocks):
        content = content.replace(f"\x00CODEBLOCK{i}\x00", block)

    # 8. 남은 HTML 태그 제거 (figcaption 등)
    # img 태그 (이미 figure 처리했지만 혹시 남은 것)
    content = re.sub(r'<img[^>]*/?\s*>', '', content)
    # 기타 inline HTML (br 등)
    content = re.sub(r'<br\s*/?>', '\n', content)
    # 남은 HTML 태그 제거
    content = re.sub(r'</?(?:strong|em|p|div|span)[^>]*>', '', content)

    # 8b. <|token|> 특수 토큰 패턴 (코드 블록 외부) → 백틱으로 감싸기
    # 먼저 코드 블록 보호
    code_blocks_8b = []
    def save_code_8b(m):
        code_blocks_8b.append(m.group(0))
        return f"\x00CODEBLOCK8B{len(code_blocks_8b)-1}\x00"
    content = re.sub(r'```[\s\S]*?```', save_code_8b, content)
    content = re.sub(r'`[^`\n]+`', save_code_8b, content)

    # <|...|> 패턴 처리
    content = re.sub(r'<\|([^|>]+)\|>', lambda m: f'`<|{m.group(1)}|>`', content)

    # 복원
    for i, block in enumerate(code_blocks_8b):
        content = content.replace(f"\x00CODEBLOCK8B{i}\x00", block)

    # 9. { } 중괄호 JSX 이스케이프 처리
    content = escape_body_braces(content)

    return content


def parse_source(src_path: str, src_type: str) -> dict:
    """소스 파일 파싱: frontmatter, h1 title, body 추출"""
    with open(src_path, encoding='utf-8') as f:
        raw = f.read()

    # GitBook frontmatter 추출
    fm_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', raw, re.DOTALL)
    date_str = ''
    if fm_match:
        fm_content = fm_match.group(1)
        desc_m = re.search(r'^description:\s*(.+)$', fm_content, re.MULTILINE)
        if desc_m:
            date_str = parse_date(desc_m.group(1).strip())
        body_raw = raw[fm_match.end():]
    else:
        body_raw = raw

    # H1 제목 추출
    h1_match = re.search(r'^#\s+(.+)$', body_raw, re.MULTILINE)
    if h1_match:
        title = h1_match.group(1).strip()
        # 본문에서 H1 제거
        body_raw = body_raw[:h1_match.start()] + body_raw[h1_match.end():]
    else:
        title = os.path.splitext(os.path.basename(src_path))[0]

    # 앞쪽 빈줄 정리
    body_raw = body_raw.lstrip('\n')

    return {
        'title': title,
        'date': date_str,
        'body_raw': body_raw,
        'src_type': src_type,
    }


def get_existing_frontmatter(target_path: str) -> dict:
    """기존 MDX 파일에서 frontmatter 추출 (title, description, tags 재사용)"""
    if not os.path.exists(target_path):
        return {}
    with open(target_path, encoding='utf-8') as f:
        content = f.read()
    fm_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not fm_match:
        return {}
    fm = fm_match.group(1)
    result = {}
    title_m = re.search(r'^title:\s*"(.*?)"', fm, re.MULTILINE)
    if title_m:
        result['title'] = title_m.group(1)
    desc_m = re.search(r'^description:\s*"(.*?)"', fm, re.MULTILINE)
    if desc_m:
        result['description'] = desc_m.group(1)
    tags_m = re.search(r'^tags:\s*(\[.*?\])', fm, re.MULTILINE | re.DOTALL)
    if tags_m:
        result['tags'] = tags_m.group(1)
    date_m = re.search(r'^publishDate:\s*(.+)$', fm, re.MULTILINE)
    if date_m:
        result['publishDate'] = date_m.group(1).strip()
    return result


def escape_body_braces(content: str) -> str:
    """본문에서 JSX 파싱 문제가 될 수 있는 { } 처리"""
    code_blocks = []
    def save_code(m):
        code_blocks.append(m.group(0))
        return f"\x00CODEBLOCK{len(code_blocks)-1}\x00"
    content = re.sub(r'```[\s\S]*?```', save_code, content)

    inline_codes = []
    def save_inline(m):
        inline_codes.append(m.group(0))
        return f"\x00INLINE{len(inline_codes)-1}\x00"
    content = re.sub(r'`[^`\n]+`', save_inline, content)

    # 중괄호 이스케이프: {text} → `{text}`
    # 단, 이미 백틱 코드 안에 있는 것, 마크다운 링크 안의 것은 제외
    # frontmatter 값은 이미 제외됨
    def escape_braces(m):
        return m.group(0).replace('{', '&#123;').replace('}', '&#125;')

    # { 가 있는 줄만 처리 (성능 고려)
    lines = content.split('\n')
    new_lines = []
    for line in lines:
        if '{' in line and '}' in line:
            # 이미 백틱 코드(`...`)로 감싸진 것은 건드리지 않음
            # 마크다운 이미지 alt 안의 {}는 건드리지 않음
            # 나머지 { } 패턴 처리
            line = re.sub(
                r'(?<![`\[])(\{[^{}\n`]+\})(?![`\]])',
                lambda m: '`' + m.group(1) + '`',
                line
            )
        new_lines.append(line)
    content = '\n'.join(new_lines)

    # 복원
    for i, block in enumerate(inline_codes):
        content = content.replace(f"\x00INLINE{i}\x00", block)
    for i, block in enumerate(code_blocks):
        content = content.replace(f"\x00CODEBLOCK{i}\x00", block)

    return content


def build_mdx(src_path: str, target_path: str, src_type: str) -> None:
    parsed = parse_source(src_path, src_type)
    existing = get_existing_frontmatter(target_path)

    # frontmatter 값 결정 (기존 MDX 우선, 없으면 소스에서)
    title = existing.get('title', parsed['title'])
    # title에서 따옴표 이스케이프
    title_escaped = title.replace('"', '\\"')

    description = existing.get('description', '')
    publish_date = existing.get('publishDate', parsed['date'])
    tags = existing.get('tags', '["Research"]' if src_type == 'research' else '["Conference", "Review"]')

    # 본문 변환
    body = convert_content(parsed['body_raw'], src_path)

    # 연속 빈줄 정리 (3줄 이상 → 2줄)
    body = re.sub(r'\n{3,}', '\n\n', body)
    body = body.strip()

    # frontmatter 조립
    frontmatter = f"""---
title: "{title_escaped}"
description: "{description}"
publishDate: {publish_date}
tags: {tags}
draft: false
---
"""

    final = frontmatter + '\n' + body + '\n'

    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(final)

    print(f"OK: {os.path.basename(src_path)} → {os.path.basename(target_path)}")


def main():
    for src_rel, target_name in FILE_MAP.items():
        src_path = os.path.join(SOURCE_BASE, src_rel)
        target_path = os.path.join(TARGET_BASE, target_name)

        if not os.path.exists(src_path):
            print(f"SKIP (not found): {src_path}")
            continue

        src_type = 'research' if src_rel.startswith('research/') else 'conference'
        build_mdx(src_path, target_path, src_type)

    print("\n변환 완료!")


if __name__ == '__main__':
    main()
