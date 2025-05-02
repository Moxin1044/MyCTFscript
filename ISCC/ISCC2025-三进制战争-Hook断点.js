// hook.js
// 使用方法：
// 1. 安装 frida 工具
// 2. 运行 frida -U -f com.example.mobile02 -l hook.js
// 3. 运行 apk
// 4. 输入ISCC{xxxxxxxxxxxx}明文，查看解密结果（主要取JNI1的值）
// 5. FLAG为：ISCC{JNI1的值+后6位值，在JADX或者JEB中看MainActivity的3进制内容}

Java.perform(function(){
    var Main = Java.use("com.example.mobile02.MainActivity");
  
    // 拦截 native 方法
    Main.stringFromJN1.implementation = function(){
      var k = this.stringFromJN1();
      console.log(">>> JNI0 key = " + k); // 输出密钥
      return k;
    };
    Main.stringFromJNI.overload('java.lang.String').implementation = function(arg){
      var out = this.stringFromJNI(arg);
      console.log(">>> JNI1(" + arg + ") = " + out); // 输出解密结果
      return out;
    };
    Main.stringFromJNl.overload('java.lang.String','java.lang.String').implementation = function(k, body){
      var out = this.stringFromJNl(k, body);
      console.log(">>> JNI2 decrypt with key="+k+" body="+body+" → " + out);
      return out;
    };
  });
  