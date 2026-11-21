/** Document offsets use UTF-16, as in CodeMirror and VS Code. */
import vocabulary from "./vocabulary.mjs";

const types = new Set(vocabulary.types);
const builtins = new Map(Object.entries(vocabulary.builtins));
const keywords = new Set(vocabulary.keywords);
const constants = new Set(vocabulary.constants);
const pattern = /\/\/[^\r\n]*|\/\*[\s\S]*?(?:\*\/|$)|"(?:\\[^\r\n]|[^\\"\r\n])*"?|'(?:\\[^\r\n]|[^\\'\r\n])*'?|[A-Za-z_]\w*|\d+(?:\.\d+)?(?:[eE][+-]?\d+)?|\.\.|==|!=|<=|>=|\+\+|--|\+=|-=|&&|\|\||[^\s]/g;
const staticSymbols = [
  ...vocabulary.keywords.map(label => ({label, kind:"keyword"})),
  ...vocabulary.types.map(label => ({label, kind:"type"})),
  ...vocabulary.constants.map(label => ({label, kind:"constant"})),
  ...Array.from(builtins, ([label, signatures]) => ({label, kind:"builtin", signatures})),
];

export function tokens(text) {
  return Array.from(text.matchAll(pattern), match => {
    const word = match[0], from = match.index;
    let kind;
    if (word.startsWith("//") || word.startsWith("/*")) kind = "comment";
    else if (word.startsWith('"')) kind = "string";
    else if (word.startsWith("'")) kind = "character";
    else if (/^\d/.test(word)) kind = "number";
    else if (types.has(word)) kind = "type";
    else if (keywords.has(word)) kind = "keyword";
    else if (constants.has(word)) kind = "constant";
    else if (/^\w/.test(word)) kind = "variable";
    else kind = "operator";
    return {word, from, to:from + word.length, kind};
  });
}

const pairs = {"(":")", "[":"]", "{":"}"};
function delimiters(items) {
  const stack = [], ends = new Map();
  for (const [i, {word}] of items.entries()) {
    if (Object.hasOwn(pairs, word)) stack.push(i);
    else if (stack.length && pairs[items[stack.at(-1)].word] === word) ends.set(stack.pop(), i);
  }
  return ends;
}

export function indexDocument(text) {
  const colored = tokens(text), items = colored.filter(t => t.kind !== "comment");
  const ends = delimiters(items), symbols = [], blocks = [], headers = [];
  const word = i => items[i]?.word;
  const endOf = i => items[ends.get(i)]?.from ?? text.length + 1;
  for (let i = 0; i < items.length; i++) {
    const t = items[i], w = t.word;
    while (blocks.length && t.from >= blocks.at(-1)) blocks.pop();
    while (headers.length && i > headers.at(-1).end) headers.pop();
    if (w === "{") blocks.push(endOf(i));
    if (w === "(" && ["for", "foreach"].includes(word(i-1))) {
      const end = ends.get(i) ?? items.length;
      headers.push({end, until:endOf(end + 1), kind:"variable"});
    }
    if (word(i+1) === "(" && builtins.has(w)) t.kind = "builtin";
    else if (word(i+1) === "(" && t.kind === "variable") t.kind = "function";
    if (!types.has(w)) continue;
    const j = word(i+1) === "[" && word(i+2) === "]" ? i+3 : i+1;
    const identifier = items[j];
    if (!identifier || !/^[A-Za-z_]\w*$/.test(identifier.word) || keywords.has(identifier.word)) continue;
    const label = identifier.word, detail = w + (j > i+1 ? "[]" : "");
    const header = headers.at(-1);
    if (word(j+1) === "(" && !blocks.length && !header) {
      const open = j+1, end = ends.get(open) ?? items.length;
      const params = items.slice(open+1, end).map(x => x.word).join(" ").replaceAll(" [ ]", "[]");
      symbols.push({label, kind:"function", detail, signatures:[params ? params.split(/ *, */) : []],
        from:0, to:text.length+1, declaration:identifier.from});
      headers.push({end, until:endOf(end+1), kind:"parameter"});
      identifier.kind = "function";
    } else {
      identifier.kind = "declaration";
      symbols.push({label, kind:header?.kind ?? "variable", detail,
        from:identifier.to, to:header?.until ?? blocks.at(-1) ?? text.length+1, declaration:identifier.from});
    }
  }
  return {text, tokens:colored, symbols, items};
}

export function atCursor(doc, offset) {
  const {text, items} = doc;
  const prefix = text.slice(0, offset).match(/[A-Za-z_]\w*$/)?.[0] ?? "";
  const suppressed = doc.tokens.some(t => (t.kind === "comment" || t.kind === "string" || t.kind === "character")
      && t.from < offset && (offset < t.to || (offset === t.to &&
      (t.word.startsWith("//") || (t.word.startsWith("/*") && !t.word.endsWith("*/"))))));
  const visible = new Map(staticSymbols.map(s => [s.label, s]));
  for (const s of doc.symbols) if (s.from <= offset && offset < s.to) visible.set(s.label, s);
  const completions = suppressed ? [] : Array.from(visible.values()).filter(s => s.label.startsWith(prefix));
  const nesting = [];
  for (let i = 0; i < items.length && items[i].from < offset; i++) {
    const w = items[i].word;
    if (Object.hasOwn(pairs,w)) nesting.push({close:pairs[w], name:w === "(" ? items[i-1]?.word : null, argument:0});
    else if (w === nesting.at(-1)?.close) nesting.pop();
    else if (w === "," && nesting.length) nesting.at(-1).argument++;
  }
  const call = nesting.findLast(s => s.close === ")" && visible.get(s.name)?.signatures);
  const signature = call && !suppressed ? {label:call.name, signatures:visible.get(call.name).signatures, argument:call.argument} : null;
  return {from:offset-prefix.length, completions, signature};
}

/** Convert the compiler's code-point offsets to editor offsets, including CRLF. */
export function diagnostics(text, payload) {
  const offsets = [0];
  for (const ch of text) offsets.push(offsets.at(-1) + ch.length);
  return [...(payload.diagnostics ?? []), ...(payload.warnings ?? []).map(w => ({...w, severity:"warning"}))].map(d => ({
    from:offsets[d.span?.start.offset ?? 0] ?? 0, to:offsets[d.span?.end.offset ?? 0] ?? text.length,
    severity:d.severity ?? "error", code:d.code, message:d.message, hint:d.help
  }));
}

export async function analyzeDocument({text, revision, config, cursor}, check) {
  const report = await check(text, config);
  const doc = indexDocument(text);
  return {revision, diagnostics:diagnostics(text, report), symbols:doc.symbols,
    ...(cursor === undefined ? {} : atCursor(doc, cursor))};
}
