const test = require("node:test");
const assert = require("node:assert/strict");
const path = require("node:path");
const fs = require("node:fs");
const tm = require("vscode-textmate");
const onig = require("vscode-oniguruma");

test("VS Code TextMate and the web editor classify the same tokens across the 50-example tour", async()=>{
  await onig.loadWASM(fs.readFileSync(require.resolve("vscode-oniguruma/release/onig.wasm")));
  const {indexDocument} = await import("../../editors/language.mjs");
  const grammar = JSON.parse(fs.readFileSync(path.join(__dirname,"../syntaxes/qutes.tmLanguage.json")));
  const registry = new tm.Registry({
    onigLib:Promise.resolve({createOnigScanner:p=>new onig.OnigScanner(p),createOnigString:s=>new onig.OnigString(s)}),
    loadGrammar:async scope=>scope===grammar.scopeName ? grammar : null
  });
  const rules = await registry.loadGrammar(grammar.scopeName);
  const scopes={type:"storage.type",builtin:"support.function",function:"entity.name.function",declaration:"variable.other.definition",
    keyword:"keyword.control",constant:"constant.language",number:"constant.numeric",string:"string.quoted.double",
    character:"string.quoted.single",comment:"comment."};
  const dir=path.join(__dirname,"../../examples/language");
  const files=fs.readdirSync(dir).filter(f=>/^\d\d_.*\.qut$/.test(f));
  assert.equal(files.length,50);
  for (const file of files) {
    const text=fs.readFileSync(path.join(dir,file),"utf8").replace(/\r\n/g,"\n");
    const tokens=indexDocument(text).tokens;
    let state=tm.INITIAL, offset=0, index=0;
    for (const line of text.split("\n")) {
      const result=rules.tokenizeLine(line,state);
      state=result.ruleStack;
      while (index<tokens.length && tokens[index].from<=offset+line.length) {
        const token=tokens[index++], expected=scopes[token.kind];
        if (!expected) continue;
        const actual=result.tokens.find(t=>t.startIndex<=token.from-offset && token.from-offset<t.endIndex);
        assert.ok(actual?.scopes.some(scope=>scope.startsWith(expected)),
          file+" "+token.word+" at "+token.from+" expected "+expected+" in "+actual?.scopes.join(", "));
      }
      offset+=line.length+1;
    }
  }
});
