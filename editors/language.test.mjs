import test from "node:test";
import assert from "node:assert/strict";
import {readdirSync,readFileSync} from "node:fs";
import {indexDocument,atCursor,diagnostics} from "./language.mjs";
import vocabulary from "./vocabulary.mjs";

test("all fifty tour examples have complete, matching source spans", () => {
  const tour = new URL("../examples/language/",import.meta.url);
  const files = readdirSync(tour).filter(n => /^\d\d_.*\.qut$/.test(n));
  assert.equal(files.length,50);
  const kinds = new Set();
  for (const file of files) {
    const text = readFileSync(new URL(file,tour),"utf8");
    let end = 0;
    for (const t of indexDocument(text).tokens) {
      assert.match(text.slice(end,t.from),/^\s*$/);
      assert.equal(text.slice(t.from,t.to),t.word);
      kinds.add(t.kind); end = t.to;
    }
    assert.match(text.slice(end),/^\s*$/);
  }
  for (const kind of ["keyword","type","builtin","function","declaration","number","character","string","comment","operator"])
    assert.ok(kinds.has(kind),kind);
});

test("incomplete calls, functions, loop scopes and shadowing",() => {
  const text = "input int n; void later(mut qubit p) { { int hidden=1; } for(int i=0;i<n;i++){float angle=pi; phase(p, ";
  const doc = indexDocument(text);
  const here = atCursor(doc,text.length);
  assert.equal(here.signature.label,"phase");
  assert.equal(here.signature.argument,1);
  const names = here.completions.map(x=>x.label);
  for (const label of ["p","i","angle","later","n",...Object.keys(vocabulary.builtins)]) assert.ok(names.includes(label),label);
  assert.ok(!names.includes("hidden"));
  const complete = indexDocument(text+"angle); } } hada");
  assert.deepEqual(atCursor(complete,complete.text.length).completions.map(c=>c.label),["hadamard"]);
  const after = indexDocument(complete.text+" ");
  for (const name of ["p","i","angle","hidden"]) assert.ok(!atCursor(after,after.text.length).completions.some(c=>c.label===name));
  assert.deepEqual(atCursor(indexDocument("// hada"),7).completions,[]);
});
test("compiler coordinates are Unicode code points, editor offsets count surrogate pairs",() => {
  const [d] = diagnostics("// 🐈\r\nreturn oops;",{diagnostics:[{span:{start:{offset:13},end:{offset:17}},code:"Q2002",message:"unknown"}]});
  assert.equal("// 🐈\r\nreturn oops;".slice(d.from,d.to),"oops");
});
