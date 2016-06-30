WechatImageDecoder
===

微信图片解密、找回撤回的图片。

实现原理
---

- 上篇：<https://zhuanlan.zhihu.com/p/21388706>
- 下篇：<https://zhuanlan.zhihu.com/p/21458386>

手机端可直接扫码查看：

![](http://zhangxiaoyang.me/themes/default/images/qrcode.jpg)

使用说明
---

```
Usage:
  python WechatImageDecoder.py [datfile]

Example:
  # PC:
  python WechatImageDecoder.py 1234567890.dat

  # Android:
  python WechatImageDecoder.py cache.data.10
```

其中，`datfile`为待解密的数据文件。
- PC端文件名类似`1234567890.dat`，存储路径为：`[X]:\Users\[USER]\Documents\WeChat Files\[WECHAT_USER]\Data`
- 手机端（Android）文件名类似`cache.data.10`，储存路径为：`/sdcard/tencent/MicroMsg/diskcache`。

如果想找回撤回的图片，可以查看文件的修改时间来选出一个候选集合，然后对其逐一使用`WechatImageDecoder`来还原。

*对于使用手机端微信的朋友，还有更加简便的方法，例如360卫士的“微信专清”功能，里面可以看到所有的聊天图片，包括被撤回的。*


免责声明
---

以上工具仅供学习交流，您一旦使用请自行承担相应的风险。


参考
---

<https://www.zhihu.com/question/35056157>


License
---

MIT
