#!/usr/bin/env node

/**
 * 微信公众号文章提取与转换工具
 * 功能：提取文章内容并转换为 Markdown 格式
 */

const { extract } = require('@extractus/article-extractor');
const TurndownService = require('turndown');

async function extractAndConvert(url) {
  try {
    // 1. 提取文章
    console.error('正在提取文章...');
    const result = await extract(url);
    
    if (!result) {
      throw new Error('文章提取失败');
    }
    
    const data = result;
    
    // 2. 转换 HTML 为 Markdown
    console.error('正在转换为 Markdown...');
    const turndownService = new TurndownService({
      headingStyle: 'atx',
      codeBlockStyle: 'fenced',
      emDelimiter: '*',
      strongDelimiter: '**',
      linkStyle: 'inlined'
    });
    
    // 自定义规则：移除样式标签
    turndownService.addRule('removeStyles', {
      filter: ['style', 'script'],
      replacement: () => ''
    });
    
    // 自定义规则：处理图片
    turndownService.addRule('images', {
      filter: 'img',
      replacement: (content, node) => {
        const src = node.getAttribute('data-src') || node.getAttribute('src') || '';
        const alt = node.getAttribute('alt') || '图片';
        return src ? `\n![${alt}](${src})\n` : '';
      }
    });
    
    const markdown = turndownService.turndown(data.msg_content || '');
    
    // 3. 构建完整的 Markdown 文档
    const output = {
      title: data.msg_title,
      author: data.msg_author || data.account_name,
      publishTime: data.msg_publish_time_str,
      description: data.msg_desc,
      cover: data.msg_cover,
      link: data.msg_link,
      content: markdown,
      fullMarkdown: generateFullMarkdown(data, markdown)
    };
    
    // 输出 JSON 格式结果
    console.log(JSON.stringify(output, null, 2));
    
  } catch (error) {
    console.error('错误:', error.message);
    process.exit(1);
  }
}

function generateFullMarkdown(data, content) {
  return `# ${data.msg_title}

**作者**: ${data.msg_author || data.account_name}  
**发布时间**: ${data.msg_publish_time_str}  
**公众号**: ${data.account_name}

${data.msg_desc ? `> ${data.msg_desc}\n` : ''}
${data.msg_cover ? `![封面](${data.msg_cover})\n` : ''}
---

${content}

---

**原文链接**: ${data.msg_link}
`;
}

// 命令行调用
if (require.main === module) {
  const url = process.argv[2];
  if (!url) {
    console.error('用法: node extract_and_convert.js <微信文章URL>');
    process.exit(1);
  }
  extractAndConvert(url);
}

module.exports = { extractAndConvert };
