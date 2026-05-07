---
name: clawd-animation-lite
description: Clawd 像素风动画生成器（轻量版）。根据用户的自然语言描述，生成1-3秒的简短clawd动画，当用户的需求的互动场景较为具体和单一，请采用轻量版本生成token消耗少、生成速度快的HTML像素风动画文件。主角是 Claude Code 的吉祥物 Clawd（像素风小螃蟹）。当用户提到 clawd、clawd 动画、像素动画、pixel animation、给 clawd 做一个小动画、让小螃蟹做某事、或任何涉及轻量化的为 Clawd 角色创建动画场景的需求时，务必使用此 skill。即使用户只是说"让 clawd 开心一下"或"做个小螃蟹的动画"，也应触发。
---

# Clawd 像素风动画生成器

你是 Clawd 像素动画的创作引擎。用户给你一句话，你生成一个可直接在浏览器打开的 HTML 动画文件。

Clawd 是 Claude Code 的吉祥物——一只像素风小螃蟹，珊瑚橙色（#CD6E58），14×8 像素的扁平可爱造型，没有嘴巴。

## 流程

1. **解析**：从描述中提取核心动作、情绪、需要的道具
2. **编排**：设计 1-2 个阶段，总时长 1-3 秒（默认 2 秒）
3. **生成**：基于下方引擎模板，只填写 `YOUR ANIMATION HERE` 区域，输出完整 HTML

## 引擎模板

生成时照抄以下代码，**只修改** `═══ YOUR ANIMATION HERE ═══` 到 `═══ LOOP ═══` 之间的区域，以及 `<title>`、info 文字和 `P` 对象中的 `ADD_COLORS_HERE` 位置。

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>TITLE</title>
<style>
  *{margin:0;padding:0;box-sizing:border-box}
  body{background:#E8E5E0;display:flex;flex-direction:column;align-items:center;justify-content:center;height:100vh;font-family:'Courier New',monospace;overflow:hidden}
  canvas{image-rendering:pixelated;image-rendering:crisp-edges;border-radius:8px;box-shadow:0 4px 24px rgba(0,0,0,.08)}
  .info{color:#999;font-size:11px;margin-top:10px;letter-spacing:1px}
</style>
</head>
<body>
<canvas id="c" width="720" height="720"></canvas>
<div class="info" id="info"></div>
<script>
const cv=document.getElementById('c'),ctx=cv.getContext('2d');

const P={
  bg:'#F9F7F4',dot:'#E0DDD8',
  sd:'#333',sm:'#888',sl:'#BBB',
  body:'#CD6E58',eye:'#000',
  w:'#FFF',blush:'#FAC8D8',pink:'#F06090',pinkDeep:'#C84060',
  // 新颜色加在这里
};

const PX=20,GW=36,GH=36;
function px(x,y,c){ctx.fillStyle=c;ctx.fillRect(x*PX,y*PX,PX,PX)}

const BODY=[
  [0,0,0,1,1,1,1,1,1,1,1,0,0,0],
  [0,0,0,1,1,1,1,1,1,1,1,0,0,0],
  [0,1,1,1,1,1,1,1,1,1,1,1,1,0],
  [0,1,1,1,1,1,1,1,1,1,1,1,1,0],
  [0,0,0,1,1,1,1,1,1,1,1,0,0,0],
  [0,0,0,1,1,1,1,1,1,1,1,0,0,0],
  [0,0,0,1,0,1,0,0,1,0,1,0,0,0],
  [0,0,0,1,0,1,0,0,1,0,1,0,0,0]
];
const EL={x:4,y:1},ER={x:9,y:1};
const EYES={forward:{dl:0,dr:0,dy:0},right:{dl:1,dr:1,dy:0},left:{dl:-1,dr:-1,dy:0},down:{dl:0,dr:0,dy:1},blink:null};
const HEART=[[1,0,1],[1,1,1],[0,1,0]];
const STARS=[
  [4,3,0],[14,2,0],[27,1,0],[31,3,1],[6,7,0],[19,5,2],[24,6,1],
  [9,10,0],[2,13,0],[33,8,0],[29,12,0],[7,16,1],[3,20,0],[30,18,1],
  [1,25,0],[33,24,0],[5,30,2],[28,28,1],[15,9,2],[21,14,1]
];

function drawBg(){
  ctx.fillStyle=P.bg;ctx.fillRect(0,0,720,720);
  for(let y=1;y<GH;y+=2)for(let x=1;x<GW;x+=2){
    ctx.fillStyle=P.dot;ctx.beginPath();ctx.arc(x*PX+10,y*PX+10,2,0,6.28);ctx.fill();
  }
}
function drawStars(f){
  ctx.textAlign='center';ctx.textBaseline='middle';
  for(const[x,y,t]of STARS){
    const tw=Math.sin(f*.08+x*.5+y*.3);
    ctx.fillStyle=t===0?(tw>0?P.sd:P.sm):t===1?(tw>.3?P.sm:P.sl):(tw>0?P.sl:P.dot);
    ctx.font=`bold ${t===0?14:10}px serif`;
    ctx.fillText('✳',x*PX+10,y*PX+10);
  }
}
function drawClawd(ox,oy,eyes='forward'){
  for(let r=0;r<8;r++)for(let c=0;c<14;c++)if(BODY[r][c])px(ox+c,oy+r,P.body);
  const e=EYES[eyes];
  if(e){px(ox+EL.x+e.dl,oy+EL.y+e.dy,P.eye);px(ox+ER.x+e.dr,oy+ER.y+e.dy,P.eye)}
}
function drawBlush(ox,oy,a){ctx.globalAlpha=a;px(ox+3,oy+2,P.blush);px(ox+10,oy+2,P.blush);ctx.globalAlpha=1}
function drawSweat(ox,oy){px(ox+13,oy,P.sl);px(ox+13,oy+1,P.sl)}
function drawExclaim(ox,oy){px(ox+7,oy-3,P.sd);px(ox+7,oy-2,P.sd);px(ox+7,oy,P.sd)}
function drawQuestion(ox,oy){px(ox+6,oy-3,P.sm);px(ox+7,oy-3,P.sm);px(ox+8,oy-3,P.sm);px(ox+8,oy-2,P.sm);px(ox+7,oy-1,P.sm)}
function drawZzz(ox,oy,t){
  ctx.globalAlpha=Math.sin(t*3)*.5+.5;ctx.fillStyle=P.sm;ctx.font='bold 14px Courier New';ctx.textAlign='left';
  ctx.fillText('z',(ox+14)*PX,(oy-1)*PX);ctx.fillText('Z',(ox+15)*PX,(oy-3)*PX);ctx.globalAlpha=1;
}
function drawSparkle(ox,oy){px(ox+3,oy+1,P.w);px(ox+5,oy+1,P.w);px(ox+8,oy+1,P.w);px(ox+10,oy+1,P.w)}
function drawClawdWave(ox,oy,eyes,side='right'){
  drawClawd(ox,oy,eyes);
  if(side==='right'){px(ox+13,oy+1,P.body);px(ox+14,oy,P.body)}
  else{px(ox+0,oy+1,P.body);px(ox-1,oy,P.body)}
}
function drawHeart(hx,hy,c){for(let r=0;r<3;r++)for(let i=0;i<3;i++)if(HEART[r][i])px(hx+i,hy+r,c)}
function drawBubble(bx,by,text){
  const tw=text.length+2;
  for(let y=0;y<3;y++)for(let x=0;x<tw;x++){
    if((y===0||y===2)&&(x===0||x===tw-1))continue;
    px(bx+x,by+y,(y===0||y===2||x===0||x===tw-1)?P.sm:P.w);
  }
  px(bx+1,by+3,P.sm);ctx.fillStyle=P.sd;ctx.font='bold 12px Courier New';ctx.textAlign='left';ctx.textBaseline='top';
  ctx.fillText(text,(bx+1)*PX+3,by*PX+7);
}

let particles=[];
function addP(x,y,c){particles.push({x,y,vx:(Math.random()-.5)*.8,vy:-Math.random()*.8-.3,life:1,c})}
function tickP(){
  for(let i=particles.length-1;i>=0;i--){
    const p=particles[i];p.x+=p.vx;p.y+=p.vy;p.vy+=.04;p.life-=.025;
    if(p.life<=0){particles.splice(i,1);continue}
    if(p.life>.15)px(Math.round(p.x),Math.round(p.y),p.c);
  }
}

function easeOut(t){return 1-Math.pow(1-t,3)}
function easeInOut(t){return t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2}
function lerp(a,b,t){return a+(b-a)*t}

// ═══ YOUR ANIMATION HERE ════════════════════════════
const FPS=30, DUR=2, TOTAL=FPS*DUR;

function getPhase(t){
  if(t<0.5) return {ph:'enter',pt:t/0.5};
  return {ph:'happy',pt:(t-0.5)/0.5};
}

function render(f){
  const t=f/TOTAL, {ph,pt}=getPhase(t);
  drawBg(); drawStars(f);
  // animation logic here
  drawClawd(11,14);
  tickP();
}
// ═══ LOOP (do not modify) ═══════════════════════════
let st=null;
function loop(ts){
  if(!st)st=ts;const el=(ts-st)/1000,lt=el%DUR,f=Math.floor(lt*FPS);
  if(lt<.05)particles=[];render(f);
  document.getElementById('info').textContent=`TITLE — ${lt.toFixed(1)}s/${DUR}s`;
  requestAnimationFrame(loop);
}
requestAnimationFrame(loop);
</script>
</body>
</html>
```

## 可用 API

| 函数 | 用途 | 参数 |
|------|------|------|
| `drawClawd(ox,oy,eyes)` | 画 Clawd | eyes: `'forward'` `'right'` `'left'` `'down'` `'blink'` |
| `drawClawdWave(ox,oy,eyes,side)` | Clawd 举起钳子 | side: `'left'` / `'right'` |
| `drawBlush(ox,oy,alpha)` | 腮红 | alpha: 0-1 |
| `drawSweat(ox,oy)` | 头侧汗滴 | — |
| `drawExclaim(ox,oy)` | 头顶感叹号 | — |
| `drawQuestion(ox,oy)` | 头顶问号 | — |
| `drawZzz(ox,oy,t)` | 睡眠 zzz | t: 当前时间进度 |
| `drawSparkle(ox,oy)` | 眼冒星星（覆盖眼睛） | — |
| `drawHeart(hx,hy,color)` | 3×3 爱心 | — |
| `drawBubble(bx,by,text)` | 对话气泡 | — |
| `addP(x,y,color)` / `tickP()` | 粒子系统 | — |
| `px(gx,gy,color)` | 画单个像素格，可自由组合画任意道具 | — |
| `easeOut(t)` / `easeInOut(t)` / `lerp(a,b,t)` | 缓动 | — |

## 动画模式库

**重要：根据用户描述选择合适的模式，不要总是套用范例的结构。**

### A. 静态表情型（适合：害羞、生气、困惑、感动）
Clawd 固定在画面中央，通过表情配件的出现/消失和眼睛方向变化传达情绪。无位移、无弹跳。
```
render: drawClawd(11,14,eyes) → 配件随 pt 渐变（如 blush alpha 从 0→0.8）
动态来源：眼睛切换 + 配件 alpha 渐变 + 微小呼吸起伏 (±1px)
```

### B. 运动位移型（适合：跑步、蹦跳、进场、飞行）
Clawd 有明显的位置移动，用 lerp+easeOut 做位移，Math.sin 做弹跳。
```
render: cx/cy 随 pt 变化 → drawClawd(cx,cy+bounce,eyes)
动态来源：位移 + 弹跳 + 可选粒子尾迹
```

### C. 道具互动型（适合：撑伞、吃东西、发现宝物、拿旗子）
先用 px() 画一个自定义道具精灵，再让 Clawd 与其互动。道具≤10×15格、≤5色。
```
render: drawProp(px,py) → drawClawd 靠近道具 → 表情变化
动态来源：道具出现/下落 + Clawd 反应（exclaim→sparkle→wave）
```

### D. 环境氛围型（适合：下雨、下雪、星空、海边）
Clawd 基本静止，重点是环境粒子/背景元素的循环动画。
```
render: drawBg → 环境粒子（雨滴/雪花/落叶）→ drawClawd 静止或微动
动态来源：大量环境粒子 + Clawd 的小幅反应（看方向、缩身体）
```

## 身体动态技巧

除了 drawClawd（静态身体）和 drawClawdWave（举钳子），还可以通过以下方式增加身体表现力：

- **呼吸起伏**：`cy + Math.round(Math.sin(f*0.1)*0.5)` 让身体微微上下浮动
- **压扁拉伸**：跳起时 cy-1（拉伸感），落地时 cy+1（压扁感）
- **倾斜**：drawClawd 后额外在一侧 px() 补像素模拟倾斜
- **交替举钳**：`drawClawdWave(ox,oy,eyes, f%30<15?'left':'right')` 实现挥手
- **粒子不只是爱心**：不同场景用不同颜色——汗滴用 P.sl、星星用 P.sd、花瓣用自定义色

## 你需要写的部分

只写 `═══ YOUR ANIMATION HERE ═══` 区域的内容：

1. **`DUR`**：动画总秒数（1-3，默认 2）
2. **道具精灵**（如需要）：二维数组 + 调色映射 + 绘制函数。控制在 10×15 格以内，颜色≤5 种
3. **`getPhase(t)`**：1-2 个阶段，返回 `{ph, pt}`
4. **`render(f)`**：动画主逻辑。调用 drawBg → drawStars → 道具 → drawClawd/drawClawdWave → 表情配件 → tickP

## 设计规范

- 画布 720×720，逻辑网格 36×36（每格 20px）
- 身体单色 `#CD6E58`，无渐变无阴影
- 情绪靠 **眼睛方向 + 表情配件 + 粒子 + 气泡** 组合表达，不要每次都用爱心粒子
- 动画首尾无缝循环
- 单 HTML 文件，零依赖，30 FPS，≤15KB
- 新道具颜色加到 `P` 对象，从 `P` 引用颜色

## 复杂度边界

适合：单角色、单场景、1-2 个动作阶段的小动画。
超出范围（告知用户简化）：多角色互动、场景切换、超过 5 秒的叙事。

## 范例 A：运动型 —— "clawd 开心蹦蹦跳"

```javascript
const FPS=30, DUR=2, TOTAL=FPS*DUR;

function getPhase(t){
  if(t<0.4) return {ph:'enter',pt:t/0.4};
  return {ph:'happy',pt:(t-0.4)/0.6};
}

function render(f){
  const t=f/TOTAL, {ph,pt}=getPhase(t);
  drawBg(); drawStars(f);

  let cx=11, cy=14, eyes='forward', bounce=0;

  if(ph==='enter'){
    cx=Math.round(lerp(-15,11,easeOut(pt)));
    bounce=Math.round(Math.sin(pt*Math.PI*4)*1.5);
  } else {
    bounce=Math.round(Math.sin(pt*Math.PI*6)*2);
    eyes=Math.sin(pt*Math.PI*6)>0.5?'blink':'forward';
    if(f%6===0) addP(cx+7+Math.random()*4, cy-2, P.pink);
    if(pt>0.3){
      const hy=cy-4-Math.round(Math.sin(pt*Math.PI*2)*3);
      drawHeart(cx+15, hy, P.pink);
    }
  }

  drawClawd(cx, cy+bounce, eyes);
  if(ph==='happy' && pt>0.2) drawBlush(cx, cy+bounce, 0.6);
  tickP();
}
```

## 范例 B：静态表情型 —— "clawd 害羞"

```javascript
const FPS=30, DUR=2, TOTAL=FPS*DUR;

function render(f){
  const t=f/TOTAL;
  drawBg(); drawStars(f);

  const cx=11, cy=14;
  // 微呼吸
  const breath=Math.round(Math.sin(f*0.15)*0.5);
  // 眼睛：先正视→慢慢看向下方
  const eyes=t<0.3?'forward':t<0.5?'right':'down';
  // 腮红渐入
  const blushAlpha=t<0.25?0:Math.min((t-0.25)*3, 0.8);

  drawClawd(cx, cy+breath, eyes);
  if(blushAlpha>0) drawBlush(cx, cy+breath, blushAlpha);
  // 后半段冒出小气泡
  if(t>0.6) drawBubble(cx+14, cy-4, '...');
  tickP();
}
```

产出文件名：描述词的英文短语，如 `shy-clawd.html`、`rainy-day.html`
