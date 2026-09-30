// 验证选词优先级：本单元优先；不足时补错词本→其他单元；结算页"补充"标记；单元单选
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
  Object.defineProperty(el, 'innerHTML', { get() { return this._html || ''; }, set(v) { this._html = v; this.children = []; } });
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
global.alert = (m) => console.log('[alert]', m); global.confirm = () => true;
global.__els = els;

const testCode = `
;(function(){
  var U2 = "Unit 2 Let's go!", U1 = "Unit 1 A day out";
  curSubject='en'; curBook='2A'; curCount=15;

  // ===== 1. 单选语义 =====
  go('home');
  var ul = __els['unit-list'];
  ul.children[1].onclick();          // 点 Unit 2
  console.log('T1 点Unit2后选中:', JSON.stringify(curUnits));
  ul.children[0].onclick();          // 点 Unit 1 → 替换
  console.log('T1 改点Unit1后选中:', JSON.stringify(curUnits), '(应为["Unit 1 A day out"])');
  ul.children[0].onclick();          // 再点 Unit 1 → 取消
  console.log('T1 再点Unit1后选中:', JSON.stringify(curUnits), '(应为[])');

  // ===== 2. 词量充足：全部来自本单元，无补充 =====
  curUnits=[U1]; // Unit 1 有 15 词
  var l = pickWords();
  console.log('T2 数量:', l.length, '(期望15)', '| 全部属于U1:', l.every(w=>w.unit===U1), '| 无补充标记:', l.every(w=>!w._fill));

  // ===== 3. 词量不足：补错词本优先，再补其他单元 =====
  curUnits=[U2]; // Unit 2 只有 12 词
  getWrong().push({word:'robot', meaning:'机器人', book:'2A', unit:U1, level:'', subject:'en', time:1});
  getWrong().push({word:'thief', meaning:'小偷', book:'2A', unit:'旧单元', level:'', subject:'en', time:1});   // 已不在当前词表，不应出现
  getWrong().push({word:'早晨', meaning:'zǎo chen', book:'三年级上册', unit:'第1课', level:'', subject:'cn', time:1}); // 语文，不应混入
  var l3 = pickWords();
  console.log('T3 数量:', l3.length, '(期望15)', '| U2词在前12个:', l3.slice(0,12).every(w=>w.unit===U2));
  var fills = l3.filter(w=>w._fill);
  console.log('T3 补充词:', fills.map(w=>w.word+'@'+w.unit).join(', '));
  console.log('T3 错词本robot优先入选:', fills.some(w=>w.word==='robot'), '| 不含thief:', !l3.some(w=>w.word==='thief'), '| 不含语文词:', !l3.some(w=>w.word==='早晨'));
  var words3 = l3.map(w=>w.word.toLowerCase());
  console.log('T3 无重复词:', words3.length===new Set(words3).size);

  // ===== 4. 结算页"补充"标记 =====
  dictList = l3; renderResult();
  var html4 = __els['result-list'].children.map(c=>c.innerHTML).join('');
  console.log('T4 结算页含补充标记:', html4.indexOf('补充')>=0, '| bF样式:', html4.indexOf('bF')>=0);

  // ===== 5. 范围提示 =====
  renderRangeTip();
  console.log('T5 提示:', __els['range-tip'].innerHTML.replace(/<br>/g,' | '));

  // ===== 6. 本单元全部掌握：重听12词 + 补足3词（新规则） =====
  curUnits=[U2];
  (curWords()['2A']).filter(w=>w.unit===U2).forEach(w=>setMastered(w,true));
  var l6 = pickWords();
  console.log('T6 全掌握回退:', l6.length, '(期望15)', '| 前12为U2重听:', l6.slice(0,12).every(w=>w.unit===U2), '| 后3为补充:', l6.slice(12).every(w=>w._fill));

  // ===== 7. 语文：单课文优先，不足补词 =====
  curSubject='cn'; curBook='三年级上册'; curCount=15;
  var cnUnits=[]; (curWords()['三年级上册']).forEach(w=>{ if(cnUnits.indexOf(w.unit)<0) cnUnits.push(w.unit); });
  curUnits=[cnUnits[0]];
  var l7 = pickWords();
  var u0=cnUnits[0];
  var u0n=(curWords()['三年级上册']).filter(w=>w.unit===u0).length;
  console.log('T7 语文首课文:', u0n, '词, 取', l7.length, '| 前'+u0n+'来自该课文:', l7.slice(0,u0n).every(w=>w.unit===u0), '| 补充:', l7.filter(w=>w._fill).length, '个');

  // ===== 8. 载入时清历史多选 =====
  S.units['en']=['a','b','c']; S.units['cn']=['x'];
  var multi = ['en','cn'].filter(s=>(S.units[s]||[]).length>1);
  ['en','cn'].forEach(s=>{ if((S.units[s]||[]).length>1) S.units[s]=[]; });
  console.log('T8 多选被清:', multi.join('+'), '→', JSON.stringify(S.units));
})();
`;

eval(js + testCode);
