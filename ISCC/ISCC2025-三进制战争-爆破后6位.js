// fast_brute_position.js
const KEY    = "密钥";
const TARGET = "3进制字符串";
// 拆成 6 段，每段 6 位
const CHUNKS = TARGET.match(/.{1,6}/g);

// 全部单字节 ASCII（0x00–0x7F）
const CHARSET = [];
for(let code=0; code<=0x7F; code++){
  CHARSET.push(String.fromCharCode(code));
}

// 用来占位的填充字符（任意 ASCII，只要是单字节即可）
const FILL = 'A';

Java.perform(()=>{
  const Main = Java.use("com.example.mobile02.MainActivity");
  const inst = Main.$new();

  let s3 = Array(CHUNKS.length);

  // 对每一个位置 i 独立爆破
  for(let i = 0; i < CHUNKS.length; i++){
    let want = CHUNKS[i];
    let found = false;

    // 构造初始 probe = ['A','A',...,'A']
    let probe = new Array(CHUNKS.length).fill(FILL);

    for(let c of CHARSET){
      probe[i] = c;                   // 把测试字符放到第 i 位
      let body = probe.join('');      // 6 字节字符串

      // native 加密会返回 36 位 → 6 段×6 字符
      let out = inst.stringFromJNl(KEY, body);
      // 取第 i 段
      let seg = out.substr(i*6, 6);
      if(seg === want){
        console.log(`✅ s3[${i}] = '${c}' (0x${c.charCodeAt(0).toString(16).padStart(2,'0')})`);
        s3[i] = c;
        found = true;
        break;
      }
    }

    if(!found){
      console.error(`❌ 位置 ${i} 未找到匹配字符，可能需要扩展 CHARSET`);
    }
  }

  let tail = s3.join('');
  console.log("→ 完整 s3 =", JSON.stringify(tail));
  console.log("→ FLAG = ISCC{xxxx" + tail + "}"); // xxxx 是 JNI1 的值
});
