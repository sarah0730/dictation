// 用 mock DOM 验证 dictation.html 核心逻辑：go('browse') 渲染 2A 词表
// 断言与页面代码放在同一 eval 作用域内，直接访问内部变量
const fs = require('fs');
const html = fs.readFileSync('dictation.html', 'utf-8');
const js = html.match(/<script>([\s\S]*?)<\/script>/)[1];

function makeEl() {
  const el = {
    children: [], style: {}, dataset: {},
    classList: {
      _s: new Set(),
      add(c) { this._s.add(c); }, remove(c) { this._s.delete(c); },
      toggle(c, f) { f === undefined ? (this._s.has(c) ? this._s.delete(c) : this._s.add(c)) : (f ? this._s.add(c) : this._s.delete(c)); },
      contains(c) { return this._s.has(c); },
    },
  };
  el.appendChild = (c) => { el.children.push(c); return c; };
  el.removeChild = (c) => { el.children = el.children.filter(x => x !== c); };
  el.addEventListener = () => {};
  el.querySelector = () => null;
  el.querySelectorAll = () => [];
  Object.defineProperty(el, 'className', { get: () => '', set: () => {} });
  Object.defineProperty(el, 'innerHTML', {
    get() { return this._html || ''; },
    set(v) { this._html = v; this.children = []; },
  });
  Object.defineProperty(el, 'textContent', { get() { return this._text || ''; }, set(v) { this._text = v; } });
  el.onclick = null;
  return el;
}
const els = {};
global.document = {
  getElementById: (id) => (els[id] = els[id] || makeEl()),
  createElement: () => makeEl(),
  body: makeEl(),
  addEventListener: () => {},
};
global.window = { scrollTo: () => {}, speechSynthesis: { getVoices: () => [] } };
global.navigator = { userAgent: 'node-test' };
global.localStorage = { _m: {}, getItem(k) { return this._m[k] || null; }, setItem(k, v) { this._m[k] = v; }, removeItem(k) { delete this._m[k]; } };
global.alert = () => {}; global.confirm = () => true;
global.__els = els;

const testCode = `
;(function(){
  // ===== 场景1：英语 2A 词表浏览 =====
  curSubject = 'en'; curBook = '2A';
  go('browse');
  var list = __els['browse-list'];
  console.log('2A 分组卡片数:', list.children.length, '(期望 8)');
  list.children.forEach(function(card, i){
    var grids = card.children.filter(function(c){ return c.children.length>0; });
    var n = grids.reduce(function(s,g){ return s+g.children.length; },0);
    console.log((i+1)+'.', card.children[0].textContent, '→', n, '词条');
  });
  var u8 = list.children[7];
  var subs8 = u8.children.filter(function(c,i){ return i>0 && c.children.length===0; }).map(function(c){ return c.textContent; });
  console.log('U8 拼读分组数:', subs8.length, '(期望 5):', subs8.join(' | '));
  var u7 = list.children[6];
  var subs = u7.children.filter(function(c,i){ return i>0 && c.children.length===0; }).map(function(c){ return c.textContent; });
  console.log('U7 话题分组数:', subs.length, '(期望 8):', subs.join(' | '));
  var sentGrid = u7.children[u7.children.length-1];
  console.log('句型词条HTML(无音标行):', sentGrid.children[0].innerHTML);
  console.log('首词条HTML:', list.children[0].children[1].children[0].innerHTML);
  console.log('view-browse 显示:', !__els['view-browse'].classList.contains('hide'), '| home 隐藏:', __els['view-home'].classList.contains('hide'));

  // ===== 场景2：首页 2A 单元显示（无四会/二会降级）=====
  go('home');
  var ul = __els['unit-list'];
  console.log('\\n首页 2A 单元数:', ul.children.length);
  console.log('单元行示例:', ul.children[0].innerHTML);
  unitAll(true);
  console.log('范围提示:', __els['range-tip'].innerHTML);

  // ===== 场景3：语文浏览页 =====
  curSubject = 'cn'; curBook = '三年级上册';
  go('browse');
  var cnList = __els['browse-list'];
  console.log('\\n语文分组卡片数:', cnList.children.length, '(期望 20)');
  console.log('语文首词条HTML:', cnList.children[0].children[1].children[0].innerHTML);
  cnList.children.slice(0,3).concat(cnList.children.slice(-2)).forEach(function(c,i){
    console.log('   ', c.children[0].textContent);
  });

  // ===== 场景4：其他册别分级显示不受影响（3A）=====
  curSubject = 'en'; curBook = '3A';
  go('home');
  console.log('\\n3A 单元行(应含四会/二会):', __els['unit-list'].children[0].innerHTML);
  console.log('页面标题:', __els['page-title'].textContent);
})();
`;

eval(js + testCode);
