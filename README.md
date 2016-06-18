WechatImageDecoder
===

微信图片解密、找回撤回的图片

PC端微信
---

```
Usage:
  python WechatImageDecoder.py [datfile] [imgfile]

Example:
  python WechatImageDecoder.py test.dat myimage.jpg

```

其中，`datfile`为待解密的dat文件，存储路径为：`[X]:\Users\[USER]\Documents\WeChat Files\[WECHAT_USER]\Data`。如果想找回撤回的图片，可以查看文件的修改时间来选出一个候选的dat文件集合，然后对其逐一使用`WechatImageDecoder`来还原。

*对于使用手机端微信的朋友，有更加简便的方法，例如360卫士的“微信专清”功能，里面可以看到所有的聊天图片，包括被撤回的。*


手机端微信（Android）
---

**TODO**


免责声明
---

以上工具仅供学习交流，您一旦使用请自行承担相应的风险。


参考
---

<https://www.zhihu.com/question/35056157>


License
---

MIT
